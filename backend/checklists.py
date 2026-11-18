import io
import posixpath
import re
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from backend.catalog import CHECKLIST_URL, plain_text, references


NAMESPACE = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class ChecklistLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href') or ''
            url = urljoin(CHECKLIST_URL, href)
            if urlparse(url).hostname == 'lassonde.yorku.ca' and urlparse(url).path.lower().endswith(('.xlsx', '.pdf')):
                self.current = {'url': url, 'parts': []}

    def handle_data(self, data):
        if self.current is not None:
            self.current['parts'].append(data)

    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            label = plain_text(' '.join(self.current['parts']))
            self.links.append({'url': self.current['url'], 'label': label})
            self.current = None


def checklist_links(markup):
    parser = ChecklistLinks()
    parser.feed(markup)
    unique = {}
    for link in parser.links:
        unique.setdefault(link['url'], link)
    return list(unique.values())


def workbook_cells(content):
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        if sum(entry.file_size for entry in archive.infolist()) > 25_000_000:
            raise ValueError('Workbook exceeds decompression budget')
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
            strings = [''.join(item.itertext()) for item in root]
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        relationships = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        paths = {item.attrib['Id']: item.attrib['Target'] for item in relationships}
        output = []
        for sheet in workbook.findall('main:sheets/main:sheet', NAMESPACE):
            relation = sheet.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            target = paths.get(relation, '')
            path = posixpath.normpath(target.lstrip('/') if target.startswith('/') else 'xl/' + target)
            if not path.startswith('xl/worksheets/'):
                continue
            root = ET.fromstring(archive.read(path))
            for row in root.findall('main:sheetData/main:row', NAMESPACE):
                cells = []
                for cell in row.findall('main:c', NAMESPACE):
                    value = cell.find('main:v', NAMESPACE)
                    text = value.text or '' if value is not None else ''
                    if cell.attrib.get('t') == 's' and text:
                        text = strings[int(text)]
                    elif cell.attrib.get('t') == 'inlineStr':
                        text = ''.join(cell.find('main:is', NAMESPACE).itertext())
                    if text.strip():
                        cells.append({'cell': cell.attrib['r'], 'text': plain_text(text)})
                if cells:
                    output.append({'sheet': sheet.attrib['name'], 'row': row.attrib['r'], 'cells': cells})
        return output


def parse_checklist(content, known_ids):
    rows = workbook_cells(content)
    mentions = []
    groups = []
    code_columns = {}
    pool_templates = set()
    current_year = None
    for row in rows:
        context = ' | '.join(cell['text'] for cell in row['cells'])
        year = re.search(r'\b(first|second|third|fourth|fifth|year\s*[1-5])\s*(?:year)?\b', context, re.I)
        if year:
            current_year = year.group(0)
        for cell in row['cells']:
            column = re.sub(r'\d+', '', cell['cell'])
            header = cell['text'].strip().lower()
            if header in {'course code', 'course codes', 'course number', 'code'}:
                code_columns.setdefault(row['sheet'], [])
                if column not in code_columns[row['sheet']]:
                    code_columns[row['sheet']].append(column)
            if header == 'courses':
                pool_templates.add(row['sheet'])
            course_refs = references(cell['text'], known_ids)
            if course_refs:
                mentions.append({'sheet': row['sheet'], 'cell': cell['cell'], 'yearHeading': current_year, 'text': cell['text'], 'context': context[:1800], 'courseIds': course_refs, 'classification': 'unreviewed-checklist-reference'})
            curriculum_cell = column in code_columns.get(row['sheet'], []) or (row['sheet'] in pool_templates and column == 'A' and bool(course_refs))
            if curriculum_cell and header not in {'course code', 'course codes', 'course number', 'code'}:
                if re.search(r'optional|elective|credits|breadth|general education|choose|selected', cell['text'], re.I):
                    kind = 'pool-or-optional'
                elif re.search(r'\bor\b', cell['text'], re.I):
                    kind = 'alternative'
                elif len(course_refs) == 1:
                    kind = 'named-course'
                else:
                    kind = 'unresolved-slot'
                groups.append({'sheet': row['sheet'], 'cell': cell['cell'], 'yearHeading': current_year, 'text': cell['text'], 'courseIds': course_refs, 'kind': kind, 'reviewStatus': 'unreviewed'})
    return {'mentions': mentions, 'courseIds': sorted({identifier for mention in mentions for identifier in mention['courseIds']}), 'entryCourseIds': sorted({identifier for group in groups for identifier in group['courseIds']}), 'groups': groups, 'status': 'references-extracted', 'curriculumColumnsDetected': code_columns, 'poolTemplateSheets': sorted(pool_templates), 'calendarInWorkbook': any('2026-2027' in cell['text'] for row in rows for cell in row['cells']), 'rowCount': len(rows), 'limitations': ['Degree map seeds come from identified Code columns, or explicit course pools in general-science templates, not prerequisite-note columns. Alternatives, pools and optional entries are candidates, not all mandatory.', 'Degree rules and course eligibility require academic review; this is not a degree audit.']}
