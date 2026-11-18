"""Offline regression checks: python -m unittest backend.test_catalog -v."""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from backend.catalog import extraction_warnings, requirement_sections
from backend.server import Catalog, handler_for


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.ids = ['LE/EECS 1000', 'LE/EECS 2000', 'LE/EECS 3000', 'SC/MATH 1000']

    def sections(self, text):
        return requirement_sections(text, self.ids)

    def test_exclusions_do_not_become_prerequisites(self):
        sections = self.sections('Prerequisites: EECS 1000. Course credit exclusions EECS 3000.')
        self.assertEqual([(s['kind'], s['references']) for s in sections], [
            ('prerequisite', ['LE/EECS 1000']), ('exclusion', ['LE/EECS 3000'])])

    def test_observed_misspelled_headings(self):
        sections = self.sections('Pre-requites: EECS 1000. Co-requsities: EECS 2000.')
        self.assertEqual([s['kind'] for s in sections], ['prerequisite', 'corequisite'])
        self.assertEqual(sections[1]['references'], ['LE/EECS 2000'])

    def test_unknown_heading_terminates_dependency(self):
        text = 'Prerequisites: EECS 1000. Prerequizzites: EECS 3000.'
        self.assertEqual(self.sections(text)[0]['references'], ['LE/EECS 1000'])
        self.assertTrue(extraction_warnings(text))

    def test_historical_rules_are_separate(self):
        sections = self.sections('Prerequisites: EECS 1000. Prior to Fall 2025: Prerequisites: EECS 3000.')
        self.assertEqual([s['kind'] for s in sections], ['prerequisite', 'historical'])
        self.assertEqual(sections[0]['references'], ['LE/EECS 1000'])

    def catalog(self):
        courses = []
        for identifier, text in zip(self.ids, [
                'Prerequisites: SC/MATH 1000.',
                'Prerequisites: EECS 1000. Course credit exclusions: EECS 3000.',
                '', 'Prerequisites: EECS 1000.']):
            courses.append({'id': identifier, 'subject': identifier.split('/')[1].split()[0],
                            'title': 'Fixture course', 'isLassondeCatalog': identifier.startswith('LE/'),
                            'requirements': self.sections(text)})
        return Catalog({'schemaVersion': '1', 'courses': courses, 'programs': [
            {'id': 'degree', 'status': 'references-extracted', 'entryCourseIds': [self.ids[1]]},
            {'id': 'pdf', 'status': 'unsupported'}]})

    def test_degree_closure_terminates_cycles_and_excludes_exclusions(self):
        catalog = self.catalog()
        self.assertEqual(catalog.scope('degree', False), {self.ids[1]})
        graph = catalog.graph({'program': ['degree']})
        self.assertEqual({c['id'] for c in graph['nodes']}, {self.ids[0], self.ids[1], self.ids[3]})
        self.assertEqual(len(graph['edges']), 3)
        self.assertTrue(all(e['kind'] == 'prerequisite' for e in graph['edges']))

    def test_invalid_scopes_never_widen_to_catalog(self):
        catalog = self.catalog()
        for program in ['missing', 'pdf']:
            with self.subTest(program=program), self.assertRaises(ValueError):
                catalog.scope(program)
        with self.assertRaises(ValueError):
            catalog.graph({'program': ['degree'], 'focus': [self.ids[2]]})

    def test_search_and_encoded_lookup(self):
        catalog = self.catalog()
        for search in ['EECS1000', 'EECS 1000']:
            result = catalog.route('/api/v1/courses', {'q': [search]})
            self.assertEqual([c['id'] for c in result['courses']], [self.ids[0]])
        self.assertEqual(catalog.route('/api/v1/courses/LE%2FEECS%201000', {})['id'], self.ids[0])
        self.assertEqual(catalog.graph({'q': ['no matches']})['nodes'], [])

    def test_http_status_and_cache_contract(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(self.catalog()))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            root = f'http://127.0.0.1:{server.server_port}'
            with urlopen(root + '/api/v1/courses/LE%2FEECS%201000') as response:
                self.assertEqual(response.headers['Cache-Control'], 'no-store')
                self.assertEqual(json.load(response)['id'], self.ids[0])
            for path, status in [('/api/v1/graph?program=pdf', 400), ('/missing', 404)]:
                with self.subTest(path=path), self.assertRaises(HTTPError) as caught:
                    urlopen(root + path)
                with caught.exception as response:
                    self.assertEqual(response.code, status)
                    self.assertIn('error', json.load(response))
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    unittest.main()
