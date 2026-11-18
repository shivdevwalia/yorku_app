import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from backend.contracts import openapi


DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'catalog.json'


class Catalog:
    def __init__(self, data):
        if data.get('schemaVersion') != '1':
            raise ValueError('Unsupported dataset schema')
        self.data = data
        self.courses = {course['id']: course for course in data['courses']}
        self.programs = {program['id']: program for program in data['programs']}

    def scope(self, program_id='', supporting=True):
        if program_id:
            if program_id not in self.programs:
                raise ValueError('Unknown degree checklist')
            program = self.programs[program_id]
            if program['status'] != 'references-extracted':
                raise ValueError('Checklist extraction unavailable; use official source')
            identifiers = set(program.get('entryCourseIds', []))
            if not identifiers:
                raise ValueError('Course Code column extraction unavailable; use official checklist')
        else:
            identifiers = {identifier for identifier, course in self.courses.items() if course.get('isLassondeCatalog', False)}
        if supporting:
            queue = list(identifiers)
            while queue:
                course = self.courses.get(queue.pop())
                if not course:
                    continue
                for section in course['requirements']:
                    if section['kind'] in {'prerequisite', 'corequisite', 'combined'}:
                        for reference in section['references']:
                            if reference not in identifiers:
                                identifiers.add(reference)
                                queue.append(reference)
        return identifiers

    def graph(self, query):
        program_id = query.get('program', [''])[0]
        supporting = query.get('supporting', ['true'])[0] == 'true'
        identifiers = self.scope(program_id, supporting)
        focus = query.get('focus', [''])[0]
        if not focus:
            search = query.get('q', [''])[0].strip().lower()
            subject = query.get('subject', [''])[0]
            seeds = {identifier for identifier in identifiers if identifier in self.courses and (not subject or self.courses[identifier]['subject'] == subject) and search in (identifier + ' ' + identifier.replace(' ', '') + ' ' + self.courses[identifier]['title']).lower()}
            visible = set(seeds)
            if supporting:
                queue = list(seeds)
                while queue:
                    course = self.courses.get(queue.pop())
                    for section in course['requirements'] if course else []:
                        if section['kind'] in {'prerequisite', 'corequisite', 'combined'}:
                            for reference in section['references']:
                                if reference in identifiers and reference not in visible:
                                    visible.add(reference)
                                    queue.append(reference)
            identifiers = visible
        if focus:
            if focus not in self.courses:
                raise ValueError('Unknown focus course')
            if focus not in identifiers:
                raise ValueError('Focus course is outside selected scope')
            ancestors = {focus}
            queue = [focus]
            while queue:
                course = self.courses.get(queue.pop())
                for section in course['requirements'] if course else []:
                    if section['kind'] in {'prerequisite', 'corequisite', 'combined'}:
                        for reference in section['references']:
                            if reference in identifiers and reference not in ancestors:
                                ancestors.add(reference)
                                queue.append(reference)
            identifiers &= ancestors
        nodes = [self.courses[identifier] for identifier in sorted(identifiers) if identifier in self.courses]
        edges = []
        for course in nodes:
            for section_index, section in enumerate(course['requirements']):
                if section['kind'] not in {'prerequisite', 'corequisite', 'combined'}:
                    continue
                for reference in section['references']:
                    if reference in identifiers:
                        edges.append({'source': reference, 'target': course['id'], 'kind': section['kind'], 'section': section_index})
        return {'nodes': nodes, 'edges': edges, 'total': len(nodes), 'semantics': 'Course references only. Edges do not mean every connected course is required; read original AND/OR and non-course conditions.'}

    def route(self, path, query):
        if path == '/api/v1/openapi.json':
            return openapi()
        if path == '/api/v1/meta':
            return {key: value for key, value in self.data.items() if key not in {'courses', 'programs'}}
        if path == '/api/v1/programs':
            return {'programs': list(self.programs.values())}
        if path == '/api/v1/graph':
            return self.graph(query)
        if path == '/api/v1/courses':
            identifiers = self.scope(query.get('program', [''])[0], query.get('supporting', ['false'])[0] == 'true')
            search = query.get('q', [''])[0].strip().lower()
            subject = query.get('subject', [''])[0]
            courses = [course for identifier, course in self.courses.items() if identifier in identifiers and (not subject or course['subject'] == subject) and search in (identifier + ' ' + identifier.replace(' ', '') + ' ' + course['title']).lower()]
            return {'courses': sorted(courses, key=lambda course: course['id']), 'total': len(courses)}
        if path.startswith('/api/v1/courses/'):
            course = self.courses.get(unquote(path.removeprefix('/api/v1/courses/')))
            if not course:
                raise KeyError('Course not found')
            return course
        raise KeyError('Endpoint not found')


def handler_for(catalog):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            try:
                payload = catalog.route(parsed.path, parse_qs(parsed.query))
                status = 200
            except ValueError as error:
                status, payload = 400, {'error': str(error)}
            except KeyError as error:
                status, payload = 404, {'error': str(error.args[0])}
            body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(body)

    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Local-only catalogue API, not a production server')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    if not DATA_PATH.exists():
        parser.error('Missing catalogue. Run python -m backend.ingest first.')
    catalog = Catalog(json.loads(DATA_PATH.read_text(encoding='utf-8')))
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(catalog))
    print(f'Local catalogue API: http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
