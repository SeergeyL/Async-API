person_find = '{ "query": { "match": { "name": "%s" } }, "size": %s, "from": %s }'

person_roles_find = {
    'actor': '{ "query": { "match_phrase": { "actors_names": "%s" } } }',
    'writer': '{ "query": { "match_phrase": { "writers_names": "%s" } } }',
    'director': '{ "query": { "match_phrase": { "director": "%s" } } }'
}
