import json
from elasticsearch import Elasticsearch

# Connect to 'http://localhost:9200'
es = Elasticsearch("http://localhost:9200")

# Define index name and settings/mappings
index_name = 'my_test'
settings = {
    'number_of_shards': 2,
    'number_of_replicas': 0
}
mappings = {
    'properties': {
        'title': {'type': 'text'},
        'identifier': {'type': 'keyword'},
        'description': {'type': 'text'}
    }
}

# Create index with defined settings/mappings
es.indices.create(index=index_name, mappings=mappings, settings=settings)

# inject data to index
body = {
    'title': 'Money Heist',
    'identifier': 'idx1',
    'description': 'This series released in 2017'
}
es.index(index=index_name, id=1, document=body)

# Get data from index
data = es.get(index=index_name, id=1)['_source']
data = json.dumps(data, indent=2)
print(data)
