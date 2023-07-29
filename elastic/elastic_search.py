from elasticsearch import Elasticsearch

from permutation_text import vector2text_processing, vector2text_processing_with_splitter
from crelu import load_crelu

timeout_ms = 60000


# this is a function that used inside of other main functions
def remove_duplicates(phrase):
    words = phrase.split()
    unique_words = []

    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    return ' '.join(unique_words)


def elastic_search_by_text(focus_index, query_text):
    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

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


def elastic_search_idea3(focus_index, query_text):
    query_string = query_text.rstrip()

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

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

    return results_dict, resp["took"]


def elastic_search_idea2(focus_index, query_text):
    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

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
                    "fuzziness": "AUTO"
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

    return results_dict, resp["took"]


def elastic_search_idea1(focus_index, query_text):
    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

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

    return results_dict, resp["took"]


def elastic_search_idea4_single_subfield(focus_index, query_text):
    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

    index_name = focus_index

    # refresh whole index
    es.indices.refresh(index=index_name)

    # prepare query text
    query_string = remove_duplicates(query_text.rstrip())
    query_list = query_string.split(' ')
    K = query_string.count('T')

    prefix_step = 20
    prefix_number = int(K / prefix_step) + 1 if (K % prefix_step != 0) else int(K / prefix_step)

    match_list = []

    for i in range(1, prefix_number + 1):
        match_list.append(' '.join(query_list[0:prefix_step * i]))

    # for search among text subfields
    data_list = [
        {
            "match": {
                "prefix" + str(i + 1) + ".disjoint": prefix
            }
        } for i, prefix in enumerate(match_list)
    ]

    # for search among keyword subfields
    # data_list = [{"match": {"prefix" + str(i + 1): prefix}} for i, prefix in enumerate(match_list)]

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

    return results_dict, resp["took"]


def elastic_search_idea4_multiple_fields(focus_index, query_text):
    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

    index_name = focus_index

    # refresh whole index
    es.indices.refresh(index=index_name)

    # prepare query text
    query_string = remove_duplicates(query_text.rstrip())
    query_list = query_string.split(' ')
    K = query_string.count('T')

    prefix_step = 20
    prefix_number = int(K / prefix_step) + 1 if (K % prefix_step != 0) else int(K / prefix_step)

    match_list = []

    for i in range(1, prefix_number + 1):
        match_list.append(' '.join(query_list[0:prefix_step * i]))

    # for search among text + keyword subfields
    data_list = [
        {
            "multi_match": {
                "query": prefix,
                "fields": ["prefix" + str(i + 1), "prefix" + str(i + 1) + ".disjoint"]
            }
        } for i, prefix in enumerate(match_list)
    ]

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

    return results_dict, resp["took"]


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
        surrogate_text = vector2text_processing_with_splitter(crelu_vector, param_k)
        # the query text that could be passed into function is like: 'T12 T12 T12 T3 T3 T4'
        return elastic_search_idea4_single_subfield(focus_index, surrogate_text[0])
        # return elastic_search_idea4_multiple_fields(focus_index, surrogate_text[0])
    else:
        print(" >>> Please clarify the indexing method <<< ")
    return

# test-case for a data with K=10
# start_time = time.time()
# s = "T11 T11 T11 T11 T11 T11 T4 T4 T4 T4 T4 T2 T2 T2 T2 T7 T7 T7 T3 T3 T1     "
# f_index = 'm_title_data_k42'
# res = elastic_search_idea4_single_subfield(f_index, s)
# print(res)
# end_time = time.time()
# duration = end_time - start_time
# print("The code took", duration, "seconds to execute.")


# path = 'dataloading/Selected dataset/103102.jpg'
# elastic_search_by_image('esm', path)
