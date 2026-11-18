import argparse
import hashlib
import json
import os
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from backend.catalog import API_BASE, CALENDAR, CATALOG_ID, CHECKLIST_URL, PARSER_VERSION, ReferenceIndex, enrich_course, normalize_index, requirement_sections, extraction_warnings
from backend.checklists import checklist_links, parse_checklist
from backend.contracts import SCHEMAS, validate


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'catalog.json'


def now():
    return datetime.now(timezone.utc).isoformat()


class Fetcher:
    def __init__(self, budget, delay):
        self.budget = budget
        self.delay = delay
        self.count = 0
        self.lock = threading.Lock()

    def get(self, url):
        if urlparse(url).hostname not in {'york.kuali.co', 'lassonde.yorku.ca'}:
            raise ValueError('Only approved official source hosts are allowed')
        with self.lock:
            if self.count >= self.budget:
                raise RuntimeError('Request budget exhausted')
            self.count += 1
            time.sleep(self.delay)
        request = urllib.request.Request(url, headers={'User-Agent': 'LassondePlannerResearch/0.1 (bounded local academic planner)', 'Accept': 'application/json,text/html,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
        with urllib.request.urlopen(request, timeout=35) as response:
            if urlparse(response.url).hostname not in {'york.kuali.co', 'lassonde.yorku.ca'}:
                raise ValueError('Unexpected redirect host')
            content = response.read(12_000_001)
            if len(content) > 12_000_000:
                raise ValueError('Response exceeds size budget')
            return content


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temporary, path)


def validate_dataset(dataset):
    courses = dataset.get('courses', [])
    identifiers = [course['id'] for course in courses]
    if not courses or len(set(identifiers)) != len(identifiers):
        raise ValueError('Empty dataset or duplicate identifiers')
    if any(course['calendar'] != CALENDAR for course in courses):
        raise ValueError('Mixed calendar versions')
    if any(course['detailStatus'] != 'unresolved' and not (course.get('sourceUrl') or '').startswith(API_BASE + '/') for course in courses):
        raise ValueError('Unexpected course provenance')
    for course in courses:
        validate(course, SCHEMAS['Course'])
    validate(dataset, SCHEMAS['Meta'])
    for program in dataset['programs']:
        validate(program, SCHEMAS['Program'])
        if program['status'] == 'references-extracted' and not program['courseIds']:
            raise ValueError(f'Empty checklist extraction: {program["label"]}')
        if program['status'] == 'references-extracted' and not program.get('entryCourseIds'):
            raise ValueError(f'No curriculum course-code column found: {program["label"]}')


def ingest(args):
    fetcher = Fetcher(args.budget, args.delay)
    previous = json.loads(DATA_PATH.read_text(encoding='utf-8')) if DATA_PATH.exists() else None
    metadata = json.loads(fetcher.get(f'{API_BASE}/public/catalogs/{CATALOG_ID}'))
    index = normalize_index(json.loads(fetcher.get(f'{API_BASE}/courses/{CATALOG_ID}')))
    searched_index = normalize_index(json.loads(fetcher.get(f'{API_BASE}/courses/{CATALOG_ID}?q=LE%2F')))
    lassonde = {identifier: {**course, 'isLassondeCatalog': True} for identifier, course in searched_index.items() if course['faculty'] == 'LE'}
    unfiltered_lassonde_count = sum(course['faculty'] == 'LE' for course in index.values())
    unfiltered_lassonde_ids = {identifier for identifier, course in index.items() if course['faculty'] == 'LE'}
    index_difference = sorted(unfiltered_lassonde_ids.symmetric_difference(lassonde))
    index.update(lassonde)
    index = ReferenceIndex(index)
    old_count = sum(course.get('isLassondeCatalog', False) for course in previous['courses']) if previous else 0
    if old_count and len(lassonde) < old_count * 0.9:
        raise ValueError('Mass catalogue loss detected; previous dataset retained')
    if len(lassonde) < 100:
        raise ValueError('Unexpectedly small Lassonde index; refusing publication')
    old_details = {course['id']: course for course in previous['courses']} if previous and previous.get('schemaVersion') == '1' else {}
    markup = fetcher.get(CHECKLIST_URL).decode('utf-8')
    links = checklist_links(markup)
    if len(links) < 20:
        raise ValueError('Unexpected checklist link loss')
    failures = []
    programs = []
    for link in links:
        label = link['label'] or Path(urlparse(link['url']).path).stem
        program = {'id': hashlib.sha256(link['url'].encode()).hexdigest()[:12], 'label': label, 'calendar': CALENDAR, 'sourceUrl': link['url'], 'checkedAt': None, 'courseIds': [], 'mentions': [], 'kind': 'planning-aid' if 'first' in label.lower() or 'winter start' in label.lower() else 'program', 'status': 'unsupported-pdf' if link['url'].lower().endswith('.pdf') else 'not-retrieved'}
        if program['status'] != 'unsupported-pdf':
            try:
                program.update(parse_checklist(fetcher.get(link['url']), index))
                program['checkedAt'] = now()
            except Exception as error:
                program['status'] = 'failed'
                failures.append({'source': link['url'], 'error': str(error)[:200]})
        programs.append(program)
    targets = set(lassonde)
    targets.update(identifier for program in programs for identifier in program['courseIds'] if identifier in index)
    result = {}

    def retrieve(identifier):
        course = index[identifier]
        cached = old_details.get(identifier)
        if not args.refresh and cached and cached['pid'] == course['pid'] and cached['detailStatus'] == 'retrieved':
            return identifier, {**cached, 'variants': course['variants'], 'requirements': requirement_sections(cached['description'], index), 'extractionWarnings': extraction_warnings(cached['description']), 'isLassondeCatalog': course['isLassondeCatalog']}, None
        try:
            detail = json.loads(fetcher.get(course['sourceUrl']))
            return identifier, enrich_course(course, detail, index, now()), None
        except Exception as error:
            return identifier, course, {'source': course['sourceUrl'], 'error': str(error)[:200]}

    with ThreadPoolExecutor(max_workers=2) as executor:
        for identifier, course, failure in executor.map(retrieve, sorted(targets)):
            result[identifier] = course
            if failure:
                failures.append(failure)
            if len(result) % 50 == 0:
                print(f'{len(result)}/{len(targets)} course records processed', flush=True)
        dependencies = {reference for course in result.values() for section in course['requirements'] if section['kind'] in {'prerequisite', 'corequisite', 'combined'} for reference in section['references'] if reference in index} - set(result)
        for identifier, course, failure in executor.map(retrieve, sorted(dependencies)):
            result[identifier] = course
            if failure:
                failures.append(failure)
    all_references = {reference for course in result.values() for section in course['requirements'] for reference in section['references']}
    all_references.update(identifier for program in programs for identifier in program['courseIds'])
    for identifier in sorted(all_references - set(result)):
        if identifier in index:
            result[identifier] = index[identifier]
        else:
            faculty, rest = identifier.split('/', 1)
            subject, number = rest.split(' ', 1)
            result[identifier] = {'id': identifier, 'faculty': faculty, 'subject': subject, 'number': number, 'title': 'Unresolved source reference', 'credits': None, 'pid': None, 'calendar': CALENDAR, 'sourceUrl': None, 'description': '', 'requirements': [], 'detailStatus': 'unresolved', 'checkedAt': None, 'isLassondeCatalog': False}
    unresolved = [course for course in result.values() if course['detailStatus'] == 'unresolved']
    dataset = {'schemaVersion': '1', 'parserVersion': PARSER_VERSION, 'catalogId': CATALOG_ID, 'calendar': CALENDAR, 'catalogTitle': metadata.get('name') or metadata.get('title') or 'York FW26/27 Undergrad Calendar', 'generatedAt': now(), 'sourceUrl': 'https://2026-2027.calendars.students.yorku.ca/academic-calendar', 'checklistSourceUrl': CHECKLIST_URL, 'courses': sorted(result.values(), key=lambda course: course['id']), 'programs': sorted(programs, key=lambda program: program['label']), 'coverage': {'lassondeIndexed': len(lassonde), 'lassondeDetails': sum(course['faculty'] == 'LE' and course['detailStatus'] == 'retrieved' for course in result.values()), 'supportingCourses': sum(course['faculty'] not in {'LE', '?'} for course in result.values()), 'unresolvedReferences': len(unresolved), 'programsExtracted': sum(program['status'] == 'references-extracted' for program in programs), 'programsLinked': len(programs), 'requests': fetcher.count, 'failures': failures}, 'limitations': ['2026-2027 catalogue only; no guarantee of current teaching-term availability.', 'Prerequisite edges are course references from labeled source text, not an AND/OR eligibility calculation.', 'Checklist references include prerequisites, alternatives and elective pools; not an approved mandatory-course list.', 'Source fields are automatically extracted and not independently academically reviewed.', 'Local research use only; downstream public-display and redistribution rights remain unresolved.']}
    dataset['coverage']['lassondeDetails'] = sum(course.get('isLassondeCatalog', False) and course['detailStatus'] == 'retrieved' for course in result.values())
    dataset['coverage']['unfilteredLassondeIndexCount'] = unfiltered_lassonde_count
    dataset['coverage']['subjects'] = sorted({course['subject'] for course in lassonde.values()})
    dataset['coverage']['indexDifferences'] = index_difference
    dataset['coverage']['lassondeSourceRecords'] = sum(len(course['variants']) for course in lassonde.values())
    dataset['limitations'].append('Multiple source records can share a course code; the displayed primary record prefers English. Alternate records remain linked and need academic reconciliation.')
    if index_difference:
        dataset['limitations'].append('Unfiltered and searched indexes disagree after normalization; the exact differences are recorded in coverage.indexDifferences. Completeness is not established.')
    validate_dataset(dataset)
    if previous:
        previous_details = sum(course['detailStatus'] == 'retrieved' for course in previous['courses'])
        current_details = sum(course['detailStatus'] == 'retrieved' for course in dataset['courses'])
        if current_details < previous_details * 0.9:
            raise ValueError('Mass detail loss; previous dataset retained')
        previous_programs = sum(program['status'] == 'references-extracted' for program in previous['programs'])
        current_programs = sum(program['status'] == 'references-extracted' for program in programs)
        if current_programs < previous_programs * 0.9:
            raise ValueError('Mass checklist extraction loss; previous dataset retained')
    atomic_json(DATA_PATH, dataset)
    print(json.dumps(dataset['coverage'], indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bounded official-source local catalogue import; no login or live timetable.')
    parser.add_argument('--budget', type=int, default=900)
    parser.add_argument('--delay', type=float, default=0.2)
    parser.add_argument('--refresh', action='store_true')
    arguments = parser.parse_args()
    if not 1 <= arguments.budget <= 1200 or arguments.delay < 0.1:
        parser.error('Budget must be 1-1200 and delay at least 0.1 seconds')
    ingest(arguments)
