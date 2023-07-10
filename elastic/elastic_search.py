from elasticsearch import Elasticsearch
import time

from models import load_model
from permutation_text import generate_permutation, generate_text_opt, vector2text_processing
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

    for hit in resp['hits']['hits']:
        hit_title = hit["_source"]["title"]
        hit_score = hit["_score"]
        results_dict[hit_title] = hit_score

    return results_dict


def elastic_search_by_vector(focus_index, vector, param_k):
    crelu_vector = load_crelu(vector)
    surrogate_text = vector2text_processing(crelu_vector, param_k)
    return elastic_search_by_text(focus_index, surrogate_text[0])




# test-case for a data with K=10
# start_time = time.time()
# s = "T1661T1661T1661T1661T1661T1661T1661T1661T1661T1661 T1065T1065T1065T1065T1065T1065T1065T1065T1065 T1335T1335T1335T1335T1335T1335T1335T1335 T715T715T715T715T715T715T715 T1751T1751T1751T1751T1751T1751 T385T385T385T385T385 T869T869T869T869 T343T343T343 T508T508 T311"
# f_index = 'data'
# elastic_searching(f_index, s)
# end_time = time.time()
# duration = end_time - start_time
# print("The code took", duration, "seconds to execute.")


# path = 'dataloading/Selected dataset/103102.jpg'
# elastic_search_by_image('esm', path)
