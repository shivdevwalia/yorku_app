import argparse
import json
from pathlib import Path


def array(items):
    return {'type': 'array', 'items': items}


def reference(name):
    return {'$ref': '#/components/schemas/' + name}


def record(properties, optional=()):
    return {'type': 'object', 'properties': properties, 'required': [key for key in properties if key not in optional]}


STRING = {'type': 'string'}
NULLABLE_STRING = {'type': ['string', 'null']}
INTEGER = {'type': 'integer', 'minimum': 0}
SCHEMAS = {
    'Requirement': record({'kind': {'enum': ['prerequisite', 'corequisite', 'combined', 'exclusion', 'crosslisting', 'historical', 'note']}, 'label': STRING, 'text': STRING, 'references': array(STRING), 'logic': {'const': 'source-text-only'}}),
    'Variant': record({'pid': STRING, 'title': STRING, 'language': NULLABLE_STRING, 'sourceIdentifier': STRING, 'sourceUrl': STRING}),
    'Course': record({'id': STRING, 'subject': STRING, 'faculty': STRING, 'number': STRING, 'title': STRING, 'credits': NULLABLE_STRING, 'description': STRING, 'requirements': array(reference('Requirement')), 'detailStatus': {'enum': ['retrieved', 'index-only', 'unresolved']}, 'calendar': STRING, 'checkedAt': NULLABLE_STRING, 'sourceUrl': NULLABLE_STRING, 'variants': array(reference('Variant')), 'language': NULLABLE_STRING, 'requirementStatus': STRING, 'isLassondeCatalog': {'type': 'boolean'}, 'extractionWarnings': array(STRING)}, optional=('variants', 'language', 'requirementStatus', 'isLassondeCatalog', 'extractionWarnings')),
    'Mention': record({'sheet': STRING, 'cell': STRING, 'text': STRING, 'context': STRING, 'courseIds': array(STRING), 'yearHeading': NULLABLE_STRING}),
    'CurriculumGroup': record({'sheet': STRING, 'cell': STRING, 'yearHeading': NULLABLE_STRING, 'text': STRING, 'courseIds': array(STRING), 'kind': STRING, 'reviewStatus': STRING}),
    'Program': record({'id': STRING, 'label': STRING, 'calendar': STRING, 'kind': {'enum': ['program', 'planning-aid']}, 'status': STRING, 'sourceUrl': STRING, 'courseIds': array(STRING), 'checkedAt': NULLABLE_STRING, 'mentions': array(reference('Mention')), 'entryCourseIds': array(STRING), 'groups': array(reference('CurriculumGroup')), 'calendarInWorkbook': {'type': 'boolean'}}, optional=('entryCourseIds', 'groups', 'calendarInWorkbook')),
    'Edge': record({'source': STRING, 'target': STRING, 'kind': {'enum': ['prerequisite', 'corequisite', 'combined']}, 'section': INTEGER}),
    'Graph': record({'nodes': array(reference('Course')), 'edges': array(reference('Edge')), 'total': INTEGER, 'semantics': STRING}),
    'Failure': record({'source': STRING, 'error': STRING}),
    'Coverage': record({'lassondeIndexed': INTEGER, 'lassondeDetails': INTEGER, 'supportingCourses': INTEGER, 'unresolvedReferences': INTEGER, 'programsExtracted': INTEGER, 'programsLinked': INTEGER, 'subjects': array(STRING), 'failures': array(reference('Failure'))}),
    'Meta': record({'schemaVersion': {'const': '1'}, 'calendar': STRING, 'generatedAt': STRING, 'sourceUrl': STRING, 'limitations': array(STRING), 'coverage': reference('Coverage')}),
    'Error': record({'error': STRING}),
}


def openapi():
    responses = {
        '/meta': reference('Meta'),
        '/programs': record({'programs': array(reference('Program'))}),
        '/courses': record({'courses': array(reference('Course')), 'total': INTEGER}),
        '/courses/{courseId}': reference('Course'),
        '/graph': reference('Graph'),
    }
    paths = {}
    for path, schema in responses.items():
        parameters = []
        if path in {'/courses', '/graph'}:
            parameters = [{'name': name, 'in': 'query', 'schema': STRING} for name in ['program', 'subject', 'q', 'supporting']]
        if path == '/graph':
            parameters.append({'name': 'focus', 'in': 'query', 'schema': STRING})
        if '{courseId}' in path:
            parameters.append({'name': 'courseId', 'in': 'path', 'required': True, 'schema': STRING, 'description': 'URL-encoded canonical ID, such as LE/EECS 2030'})
        paths['/api/v1' + path] = {'get': {'parameters': parameters, 'responses': {'200': {'description': 'Local research catalogue result', 'content': {'application/json': {'schema': schema}}}, '400': {'description': 'Invalid or unsupported scope', 'content': {'application/json': {'schema': reference('Error')}}}, '404': {'description': 'Not found', 'content': {'application/json': {'schema': reference('Error')}}}}}}
    return {'openapi': '3.1.0', 'info': {'title': 'Lassonde Atlas local API', 'version': '1.0.0'}, 'paths': paths, 'components': {'schemas': SCHEMAS}}


def validate(value, schema, path='$'):
    if '$ref' in schema:
        return validate(value, SCHEMAS[schema['$ref'].split('/')[-1]], path)
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(path + ': invalid enum')
    if 'const' in schema and value != schema['const']:
        raise ValueError(path + ': invalid constant')
    expected = schema.get('type')
    if isinstance(expected, list):
        if value is None and 'null' in expected:
            return
        return validate(value, {**schema, 'type': next(kind for kind in expected if kind != 'null')}, path)
    predicates = {'string': lambda item: isinstance(item, str), 'integer': lambda item: isinstance(item, int) and not isinstance(item, bool), 'boolean': lambda item: isinstance(item, bool), 'object': lambda item: isinstance(item, dict), 'array': lambda item: isinstance(item, list)}
    if expected in predicates and not predicates[expected](value):
        raise ValueError(path + ': expected ' + expected)
    if expected == 'integer' and value < schema.get('minimum', value):
        raise ValueError(path + ': below minimum')
    if expected == 'object':
        for key in schema.get('required', []):
            if key not in value:
                raise ValueError(path + ': missing ' + key)
        for key, child in schema.get('properties', {}).items():
            if key in value:
                validate(value[key], child, path + '.' + key)
    if expected == 'array':
        for index, item in enumerate(value):
            validate(item, schema['items'], path + '[' + str(index) + ']')


def typescript_type(schema):
    if '$ref' in schema:
        return schema['$ref'].split('/')[-1]
    if 'enum' in schema:
        return ' | '.join(json.dumps(value) for value in schema['enum'])
    if 'const' in schema:
        return json.dumps(schema['const'])
    kind = schema['type']
    if isinstance(kind, list):
        return ' | '.join(typescript_type({'type': item}) for item in kind)
    if kind == 'array':
        return '(' + typescript_type(schema['items']) + ')[]'
    if kind == 'object':
        fields = [key + ('' if key in schema.get('required', []) else '?') + ': ' + typescript_type(value) + ';' for key, value in schema['properties'].items()]
        return '{\n  ' + '\n  '.join(fields) + '\n}'
    return {'string': 'string', 'integer': 'number', 'boolean': 'boolean', 'null': 'null'}[kind]


def typescript():
    return '\n\n'.join('export type ' + name + ' = ' + typescript_type(schema) + ';' for name, schema in SCHEMAS.items()) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-types', action='store_true')
    args = parser.parse_args()
    if args.check_types:
        path = Path(__file__).resolve().parents[1] / 'frontend' / 'lib' / 'types.ts'
        if path.read_text(encoding='utf-8') != typescript():
            raise SystemExit('Frontend contract types differ from OpenAPI schemas')
        print('Frontend types match OpenAPI schemas')
    else:
        print(json.dumps(openapi(), indent=2))
