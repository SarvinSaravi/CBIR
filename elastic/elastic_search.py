import json
from elasticsearch import Elasticsearch

# Connect to 'http://localhost:9200'
es = Elasticsearch("http://localhost:9200")

index_name = 'test3'

# refresh whole index
es.indices.refresh(index=index_name)

my_query = {
    "bool": {
        "should": [
            {
                "match": {
                    "pos5": "T4T4T4T4T4"
                }
            },
            {
                "match": {
                    "pos4": "T2T2T2T2"
                }
            },
            {
                "match": {
                    "pos3": "T12T12T12"
                }
            },
            {
                "match": {
                    "pos2": "T5T5"
                }
            },
            {
                "match": {
                    "pos1": "T2"
                }
            }
        ],
        "minimum_should_match": 1
    }
}

resp = es.search(index=index_name, query=my_query)
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print("score of this result is %s" % hit["_score"])
    print(hit["_source"])
