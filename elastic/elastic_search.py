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
        # the query text that could be passed into function is like: 'T12 T12 T12 T3 T3 T4'
        return elastic_search_idea3(focus_index, surrogate_text[0])
    elif indexing_method == 'fuzzy_search':
        surrogate_text = vector2text_processing(crelu_vector, param_k)
        # the query text that could be passed into function is like: 'T12T12T12 T3T3 T4'
        return elastic_search_idea2(focus_index, surrogate_text[0])
    elif indexing_method == 'remove_frequency':
        surrogate_text = vector2text_processing_with_splitter(crelu_vector, param_k)
        # the query text that could be passed into function is like: 'T12 T12 T12 T3 T3 T4'
        return elastic_search_idea1(focus_index, surrogate_text[0])
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


def elastic_search_idea2(focus_index, query_text):

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200")

    index_name = focus_index

    # refresh whole index
    es.indices.refresh(index=index_name)

    query_string = query_text.rstrip()
    query_split = query_string.split(' ')
    query_split = [st.split('T') for st in query_split]

    query_list = []

    for position_list in query_split:
        position_code_phrase = ''
        for codeword in position_list:
            if codeword != '':
                position_code_phrase = position_code_phrase + 'T' + codeword + ' '
        query_list.append(position_code_phrase.rstrip())

    data_list = [
        {
            "match": {
                "text_code": {
                    "query": q,
                    "fuzziness": "1"
                }
            }
        } for q in query_list
    ]

    my_query = {
        "bool": {
            "should": data_list
        }
    }

    results_dict = {}

    resp = es.search(index=index_name, query=my_query)
    for hit in resp['hits']['hits']:
        hit_title = hit["_source"]["title"]
        hit_score = hit["_score"]
        results_dict[hit_title] = hit_score

    return results_dict


def elastic_search_idea1(focus_index, query_text):
    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200")

    index_name = focus_index

    # refresh whole index
    es.indices.refresh(index=index_name)

    # prepare query text
    query_string = remove_duplicates(query_text.rstrip())

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


# this is a function that used inside of other main functions
def remove_duplicates(phrase):
    words = phrase.split()
    unique_words = []

    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    return ' '.join(unique_words)


# test-case for a data with K=10
# start_time = time.time()
# s = "T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1879 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T1083 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T267 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1465 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1298 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T1000 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T15 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T703 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T1215 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T828 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T200 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T884 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T74 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T90 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1348 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1440 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T1106 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T137 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T383 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T731 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T891 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T789 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T616 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1119 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1071 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T1810 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T2034 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1981 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T1540 T17 T17 T17 T17 T17 T17 T17 T17 T17 T17 T17 T17 T17 T1327 T1327 T1327 T1327 T1327 T1327 T1327 T1327 T1327 T1327 T1327 T1327 T1064 T1064 T1064 T1064 T1064 T1064 T1064 T1064 T1064 T1064 T1064 T30 T30 T30 T30 T30 T30 T30 T30 T30 T30 T1694 T1694 T1694 T1694 T1694 T1694 T1694 T1694 T1694 T50 T50 T50 T50 T50 T50 T50 T50 T549 T549 T549 T549 T549 T549 T549 T10 T10 T10 T10 T10 T10 T783 T783 T783 T783 T783 T1547 T1547 T1547 T1547 T236 T236 T236 T595 T595 T696"
# f_index = 'm_title_data_k42'
# res = elastic_search_idea1(f_index, s)
# print(res)
# end_time = time.time()
# duration = end_time - start_time
# print("The code took", duration, "seconds to execute.")


# path = 'dataloading/Selected dataset/103102.jpg'
# elastic_search_by_image('esm', path)
