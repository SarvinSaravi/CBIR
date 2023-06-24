from elasticsearch import Elasticsearch
import time


def elastic_searching(focus_index, query_text):
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

    resp = es.search(index=index_name, query=my_query)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print(("Picture ID: %s" % hit["_id"]))
        print("score of this result is %s" % hit["_score"])
        # print(hit["_source"]["title"])
        print(hit["_source"])
        print()


# test-case for a data with K=10
# start_time = time.time()
# s = "T1661T1661T1661T1661T1661T1661T1661T1661T1661T1661 T1065T1065T1065T1065T1065T1065T1065T1065T1065 T1335T1335T1335T1335T1335T1335T1335T1335 T715T715T715T715T715T715T715 T1751T1751T1751T1751T1751T1751 T385T385T385T385T385 T869T869T869T869 T343T343T343 T508T508 T311"
# f_index = 'data'
# elastic_searching(f_index, s)
# end_time = time.time()
# duration = end_time - start_time
# print("The code took", duration, "seconds to execute.")

