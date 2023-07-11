from elasticsearch import Elasticsearch


def elastic_indexing(title_list, data_list, focus_index, indexing_method, shard_number=2, replica_number=0 ):
    if indexing_method == 'same_exact_phrase_with_separator':
        return elastic_indexing_idea3(title_list, data_list, focus_index, shard_number, replica_number)
    elif indexing_method == 'fuzzy_search':
        print(' to do ')  # todo
    elif indexing_method == 'remove_frequency':
        print(' to do ')  # todo
    elif indexing_method == 'prefix_search':
        print(' to do ')  # todo
    else:
        print(" >>> Please clarify the indexing method <<< ")
    return


def elastic_indexing_with_titles(title_list, data_list, k, focus_index, shard_number=2, replica_number=0):
    # preparation mappings
    str_lst = [st.rstrip() for st in data_list]
    K = k
    data = {
        'title': {'type': 'keyword'}
    }
    index_counting_list = list(reversed(range(1, K + 1)))

    for i in index_counting_list:
        key = 'pos' + str(i)
        data[key] = {'type': 'keyword'}

    mappings = {
        'properties': data
    }

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
        data['title'] = title_list[tmp_id - 1]
        for i, x in zip(index_counting_list, mid_list):
            key = 'pos' + str(i)
            data[key] = x

        es.index(index=index_name, id=str(tmp_id), document=data)
        tmp_id += 1


def elastic_indexing_idea3(title_list, data_list, focus_index, shard_number, replica_number):
    # preparation mappings
    str_lst = [st.rstrip() for st in data_list]

    mappings = {
        'properties': {
            'title': {'type': 'keyword'},
            'text_code': {'type': 'text'}
        }
    }

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
    for text_code, title in zip(str_lst, title_list):
        data = {
            'title': title,
            'text_code': text_code
        }
        es.index(index=index_name, id=str(tmp_id), document=data)
        tmp_id += 1


# test-cases
# str_list = [
#     'T4T4T4T4T4 T2T2T2T2 T7T7T7 T3T3 T1     ',
#     'T8T8T8T8T8 T7T7T7T7 T5T5T5 T1T1 T2     ',
#     'T10T10T10T10T10 T8T8T8T8 T7T7T7 T5T5 T6     '
# ]
# elastic_indexing(str_list, 5, 'test7')
#
# t_list = ['img1.jpg', 'img2.jpg', 'img3.jpg']
# elastic_indexing_idea3(t_list, str_list, 'test4idea3')
