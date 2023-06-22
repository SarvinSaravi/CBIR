import json
from elasticsearch import Elasticsearch


def elastic_indexing(data_list, k, focus_index, shard_number=2, replica_number=0):
    # preparation mappings
    str_lst = [st.rstrip() for st in data_list]
    K = k
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
    index_name = focus_index
    settings = {
        'number_of_shards': shard_number,
        'number_of_replicas': replica_number
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
    print()


str_list = ['T4T4T4T4T4 T2T2T2T2 T7T7T7 T3T3 T1     ',
            'T8T8T8T8T8 T7T7T7T7 T5T5T5 T1T1 T2     ',
            'T10T10T10T10T10 T8T8T8T8 T7T7T7 T5T5 T6     '
            ]

elastic_indexing(str_list, 5, 'test7')
