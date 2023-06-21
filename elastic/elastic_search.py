import json
from elasticsearch import Elasticsearch

# Connect to 'http://localhost:9200'
es = Elasticsearch("http://localhost:9200")

index_name = 'test3'

# refresh whole index
es.indices.refresh(index=index_name)

query_string = 'T42T42T42T42T42 T32T32T32T32 T12T12T12 T95T95 T2'
query_list = query_string.split(' ')

data_list = [{"match": {"pos" + str(i): pos}} for i, pos in enumerate(reversed(query_list), start=1)]


my_query2 = {
    "bool": {
        "should": data_list, "minimum_should_match": 1
    }
}

resp = es.search(index=index_name, query=my_query2)
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print("score of this result is %s" % hit["_score"])
    print(hit["_source"])
