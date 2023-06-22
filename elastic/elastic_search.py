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
        print("score of this result is %s" % hit["_score"])
        print(hit["_source"])
    print()


# s = 'T4T4T4T4T4 T2T2T2T2 T5T5T5 T1T1 T1017'
# f_index = 'test'
# elastic_searching(f_index, s)
