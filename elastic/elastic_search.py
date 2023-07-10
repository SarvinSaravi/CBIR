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
    # print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        hit_title = hit["_source"]["title"]
        hit_score = hit["_score"]
        results_dict[hit_title] = hit_score

    return results_dict


def elastic_search_by_vector(focus_index, vector, param_k):
    crelu_vector = load_crelu(vector)
    surrogate_text = vector2text_processing(crelu_vector, param_k)
    return elastic_search_by_text(focus_index, surrogate_text[0])


def elastic_search_idea3(focus_index, vector, param_k):
    permutation_vector = generate_permutation(vector)
    surrogate_text = generate_text_opt(permutation_vector, k=param_k)

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200")

    index_name = focus_index

    # refresh whole index
    es.indices.refresh(index=index_name)

    my_query = {
        "match": {
            "text_code": surrogate_text
        }
    }

    results_dict = {}

    resp = es.search(index=index_name, query=my_query)
    # print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        # print(("Picture ID: %s" % hit["_id"]))
        # print("score of this result is %s" % hit["_score"])
        # print(hit["_source"]["title"])
        # print(hit["_source"])
        hit_id = hit["_id"]
        hit_score = hit["_score"]
        results_dict[hit_id] = hit_score

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
