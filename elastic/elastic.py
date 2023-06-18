import json
from elasticsearch import Elasticsearch

# Connect to 'http://localhost:9200'
es = Elasticsearch("http://localhost:9200")

data = es.get(index="test", id=2)['_source']
data = json.dumps(data, indent=2)
print(data)
