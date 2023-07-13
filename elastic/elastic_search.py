from elasticsearch import Elasticsearch
# import time

from permutation_text import vector2text_processing, vector2text_processing_with_splitter
from crelu import load_crelu


def elastic_search_by_text(focus_index, query_text):
    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200")

    index_name = focus_index

    # refresh whole index
    es.indices.refresh(index=index_name)

    query_string = query_text.rstrip()
    query_list = query_string.split(' ')

    data_list = [{"match": {"pos" + str(i): pos}} for i, pos in enumerate(reversed(query_list), start=1)]

    my_query = {
        "bool": {
            "should": data_list, "minimum_should_match": 1
        }
    }

    results_dict = {}

    resp = es.search(index=index_name, query=my_query)
    # print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        hit_title = hit["_source"]["title"]
        hit_score = hit["_score"]
        results_dict[hit_title] = hit_score

    return results_dict


def elastic_search_by_vector(focus_index, vector, param_k, indexing_method):
    crelu_vector = load_crelu(vector)
    if indexing_method == 'same_exact_phrase_with_separator':
        surrogate_text = vector2text_processing_with_splitter(crelu_vector, param_k)
        return elastic_search_idea3(focus_index, surrogate_text[0])
    elif indexing_method == 'fuzzy_search':
        print(' to do ')  # todo
    elif indexing_method == 'remove_frequency':
        print(' to do ')  # todo
    elif indexing_method == 'prefix_search':
        print(' to do ')  # todo
    else:
        print(" >>> Please clarify the indexing method <<< ")
    return


def elastic_search_idea3(focus_index, query_text):
    query_string = query_text.rstrip()

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200")

    index_name = focus_index

    # refresh whole index
    es.indices.refresh(index=index_name)

    my_query = {
        "match": {
            "text_code": query_string
        }
    }

    results_dict = {}

    resp = es.search(index=index_name, query=my_query)
    for hit in resp['hits']['hits']:
        hit_title = hit["_source"]["title"]
        hit_score = hit["_score"]
        results_dict[hit_title] = hit_score

    return results_dict

# test-case for a data with K=10
# start_time = time.time()
# f_index = 'title_data_k42'
# res = elastic_search_idea3(f_index, s, param_k=42)
# print(res)
# end_time = time.time()
# duration = end_time - start_time
# print("The code took", duration, "seconds to execute.")


# path = 'dataloading/Selected dataset/103102.jpg'
# elastic_search_by_image('esm', path)
