import json
from elasticsearch import Elasticsearch
import pandas as pd
import csv

# preparation mappings
str_lst = ['T4T4T4T4T4 T2T2T2T2 T7T7T7 T3T3 T1     ',
           'T8T8T8T8T8 T7T7T7T7 T5T5T5 T1T1 T2     ',
           'T10T10T10T10T10 T8T8T8T8 T7T7T7 T5T5 T6     '
           ]

str_lst = [st.rstrip() for st in str_lst]
K = 5
data = {}
index_counting_list = list(reversed(range(1, K + 1)))

for i in index_counting_list:
    key = 'pos' + str(i)
    data[key] = {'type': 'keyword'}

mappings = {
    'properties': data
}

json_mappings = json.dumps(mappings, indent=4)
print(json_mappings)


# Connect to 'http://localhost:9200'
es = Elasticsearch("http://localhost:9200")

# Define index name and settings/mappings
index_name = 'test3'
settings = {
    'number_of_shards': 2,
    'number_of_replicas': 0
}

# Create index with defined settings/mappings
es.indices.create(index=index_name, mappings=mappings, settings=settings)

# inject data to index
tmp_id = 1
for st in str_lst:
    mid_list = st.split(' ')
    # mid_list.reverse()
    for i, x in zip(index_counting_list, mid_list):
        key = 'pos' + str(i)
        data[key] = x

    es.index(index=index_name, id=tmp_id, document=data)
    tmp_id += 1

