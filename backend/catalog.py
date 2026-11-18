import html
import re
from html.parser import HTMLParser


CATALOG_ID = '691dc968c6306e23358308fc'
CALENDAR = '2026-2027'
API_BASE = 'https://york.kuali.co/api/v1/catalog'
CHECKLIST_URL = 'https://lassonde.yorku.ca/student-life/2026-2027-program-checklists'
PARSER_VERSION = '1.4.0'
COURSE_PATTERN = re.compile(r'(?<![A-Z])(?:(?P<faculty>[A-Z]{2}(?:\s*/\s*[A-Z]{2})*)(?:\s*/\s*|\s+(?=[A-Z]{3,5}\s*\d)))?(?P<subject>[A-Z]{2,5})\s*/?\s*(?P<number>\d{4})(?!\d)')
ABBREVIATED_COURSE = re.compile(r'\s*(?:,\s*(?:(?:and|or)\s+)?|(?:and|or)\s+|/\s*)(?P<number>\d{4})(?!\d|\.\d|\s*(?:credits?|credit hours?)\b)', re.IGNORECASE)
PREREQUISITE_LABEL = r'pre[\-\u2010\u2011]?(?:requis(?:ite|te)|requite)(?:s|\(s\))?'
COREQUISITE_LABEL = r'co[\-\u2010\u2011]?(?:requis(?:ite|te)|requsitie)(?:s|\(s\))?'
SECTION_PATTERN = re.compile(r'(?i)\b(?P<label>' + PREREQUISITE_LABEL + r'\s*(?:and|or|/)\s*' + COREQUISITE_LABEL + r'|' + PREREQUISITE_LABEL + r'|' + COREQUISITE_LABEL + r'|course\s+credit\s+exclusions?|credit\s+exclusions?|cross-?listed(?:\s+(?:to|with|as))?|previously\s+offered\s+as|notes?|recommended(?:\s+preparation)?|not\s+open\s+to|open\s+to)(?:\s*:|\s+include\s+|\s+are\s+|\s+(?=(?:[A-Z]{2}\s*/\s*)?[A-Z]{2,5}\s*\d{4})|\s+(?=(?:cumulative|completion|permission|minimum|one|any|none)\b)|\s+(?=and\s+previously\b|\d{4}\b))')
REQUIREMENT_LIKE_PATTERN = re.compile(r'(?i)\b(?:pre|co)[\-\u2010\u2011]?[a-z()]*req[a-z()]*\s*:')
HISTORY_PATTERN = re.compile(r'(?i)\b(?:prior\s+to|before)\s+(?:fall|winter|summer|september|january|may|\d)[^:\n]{0,55}:')


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in {'br', 'p', 'div', 'li'}:
            self.parts.append('\n')


def plain_text(value):
    parser = PlainText()
    parser.feed(str(value or ''))
    return re.sub(r'[ \t]+', ' ', html.unescape(''.join(parser.parts))).strip()


def course_id(faculty, subject, number):
    return f'{faculty}/{subject.strip()} {number}'


class ReferenceIndex(dict):
    def __init__(self, values):
        super().__init__(values)
        self.subjects = set()
        self.candidates = {}
        for identifier in self:
            name = identifier.split('/')[1]
            self.subjects.add(name.split()[0])
            self.candidates.setdefault(name, []).append(identifier)


def references(text, known_ids):
    found = []
    resolver = known_ids if isinstance(known_ids, ReferenceIndex) else ReferenceIndex(dict.fromkeys(known_ids))
    for match in COURSE_PATTERN.finditer(text):
        faculty, subject, number = match.group('faculty', 'subject', 'number')
        if not faculty and subject not in resolver.subjects:
            continue
        numbers = [number]
        end = match.end()
        while abbreviated := ABBREVIATED_COURSE.match(text, end):
            numbers.append(abbreviated.group('number'))
            end = abbreviated.end()
        for number in numbers:
            candidates = resolver.candidates.get(f'{subject} {number}', [])
            # Multiple explicit faculties are not interchangeable identities.
            if faculty:
                identifier = course_id('?' if '/' in faculty else faculty, subject, number)
            else:
                identifier = candidates[0] if len(candidates) == 1 else f'?/{subject} {number}'
            if identifier not in found:
                found.append(identifier)
    return found


def requirement_sections(description, known_ids):
    matches = list(SECTION_PATTERN.finditer(description))
    history = list(HISTORY_PATTERN.finditer(description))
    unknown = [candidate for candidate in REQUIREMENT_LIKE_PATTERN.finditer(description) if not any(match.start() <= candidate.start() and candidate.end() <= match.end() for match in matches)]
    sections = []
    for index, match in enumerate(matches):
        label = match.group('label').lower()
        text = description[match.end():matches[index + 1].start() if index + 1 < len(matches) else len(description)].strip()
        boundaries = [boundary.start() for boundary in history + unknown if match.end() <= boundary.start() < (matches[index + 1].start() if index + 1 < len(matches) else len(description))]
        if boundaries:
            text = description[match.end():min(boundaries)].strip()
        historical = any(boundary.end() <= match.start() for boundary in history)
        if historical or 'previously' in label:
            kind = 'historical'
        elif 'exclusion' in label:
            kind = 'exclusion'
        elif 'cross' in label:
            kind = 'crosslisting'
        elif re.search(PREREQUISITE_LABEL, label) and re.search(COREQUISITE_LABEL, label):
            kind = 'combined'
        elif re.search(COREQUISITE_LABEL, label):
            kind = 'corequisite'
        elif re.search(PREREQUISITE_LABEL, label):
            kind = 'prerequisite'
        else:
            kind = 'note'
        sections.append({'kind': kind, 'label': ('Historical: ' if historical else '') + match.group('label'), 'text': text, 'references': references(text, known_ids), 'logic': 'source-text-only'})
    return sections


def extraction_warnings(description):
    matches = list(SECTION_PATTERN.finditer(description))
    warnings = ['Unrecognized requirement-like heading: ' + candidate.group().strip() for candidate in REQUIREMENT_LIKE_PATTERN.finditer(description) if not any(match.start() <= candidate.start() and candidate.end() <= match.end() for match in matches)]
    for match in COURSE_PATTERN.finditer(description):
        if '/' in (match.group('faculty') or ''):
            warnings.append('Ambiguous faculty in course reference: ' + match.group().strip())
        if re.match(r'\s*(?:[-–—]|to\b|through\b)\s*\d{4}\b', description[match.end():], re.IGNORECASE):
            warnings.append('Unsupported abbreviated course range: ' + description[match.start():match.end() + 30].strip())
    return warnings


def normalize_index(rows):
    output = {}
    for row in sorted(rows, key=lambda item: (item.get('languageOfInstruction', {}).get('name') != 'English', item.get('pid', ''))):
        subject = row.get('subjectCode', {}).get('name', '').strip()
        match = re.match(r'^[A-Z]{2}\s*/\s*[A-Z]{2,5}\s*(\d{4})(?!\d)', row.get('__catalogCourseId', ''))
        if '/' not in subject or not match or not row.get('pid'):
            continue
        faculty, subject_name = subject.split('/', 1)
        identifier = course_id(faculty, subject_name, match.group(1))
        variant = {'pid': row['pid'], 'title': plain_text(row.get('title')), 'language': row.get('languageOfInstruction', {}).get('name'), 'sourceIdentifier': row.get('__catalogCourseId'), 'sourceUrl': f'{API_BASE}/course/{CATALOG_ID}/{row["pid"]}'}
        if identifier in output:
            if row['pid'] != output[identifier]['pid']:
                output[identifier]['variants'].append(variant)
            continue
        output[identifier] = {'id': identifier, 'subject': subject_name.strip(), 'faculty': faculty, 'number': match.group(1), 'title': plain_text(row.get('title')), 'pid': row['pid'], 'sourceUrl': f'{API_BASE}/course/{CATALOG_ID}/{row["pid"]}', 'calendar': CALENDAR, 'detailStatus': 'index-only', 'description': '', 'credits': None, 'requirements': [], 'checkedAt': None, 'isLassondeCatalog': False, 'variants': [variant]}
    return output


def enrich_course(course, detail, known_ids, checked_at):
    if detail.get('pid') != course['pid']:
        raise ValueError('Detail PID does not match index')
    description = plain_text(detail.get('description'))
    credits = detail.get('credits', {})
    return {**course, 'title': plain_text(detail.get('title')) or course['title'], 'description': description, 'credits': credits.get('value'), 'creditRange': credits.get('credits'), 'requirements': requirement_sections(description, known_ids), 'detailStatus': 'retrieved', 'checkedAt': checked_at, 'effectiveStart': detail.get('dateStart'), 'campus': detail.get('campusLocation', {}), 'language': detail.get('languageOfInstruction', {}).get('name'), 'requirementStatus': 'source-text-extracted' if SECTION_PATTERN.search(description) else 'no-labeled-rule-found', 'extractionWarnings': extraction_warnings(description)}
