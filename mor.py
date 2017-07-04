#!/usr/bin/python27
from elasticsearch import Elasticsearch


def get_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []
    for key, value in search_dict.iteritems():
        if key == field:
            fields_found.append(value)
        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)
    print fields_found
    return fields_found

es = Elasticsearch(['http://10.200.81.223:9200'])
worldmate = es.indices.get('worldmate')
prompt = raw_input('Enter search name: ')
if prompt != '':
    found = get_recursively(worldmate, prompt)
    print 'name:%s has hits:%s' % (prompt, len(found))
else:
    hits = get_recursively(worldmate, 'hits')
    print 'found total hits:%s' % (len(hits))
