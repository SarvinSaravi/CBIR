from elasticsearch import Elasticsearch


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
        print(hit["_source"])
    print()

# test-case for a data with K=10
s = 'T757T757T757T757T757T757T757T757T757T757 T975T975T975T975T975T975T975T975T975 T920T920T920T920T920T920T920T920 T569T569T569T569T569T569T569 T1774T1774T1774T1774T1774T1774 T436T436T436T436T436 T651T651T651T651 T792T792T792 T272T272 T183                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      '
f_index = 'data'
elastic_searching(f_index, s)
