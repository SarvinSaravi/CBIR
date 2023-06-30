from elasticsearch import Elasticsearch
import time

from models import load_model
from permutation_text import vector2text_processing


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

    resp = es.search(index=index_name, query=my_query)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print(("Picture ID: %s" % hit["_id"]))
        print("score of this result is %s" % hit["_score"])
        # print(hit["_source"]["title"])
        print(hit["_source"])
        print()


def elastic_search_by_vector(focus_index, vector):
    surrogate_text = vector2text_processing(vector)
    return elastic_search_by_text(focus_index, surrogate_text)


def elastic_search_by_image(focus_index, img_path):
    dataset_path = img_path
    image_size = (224, 224)

    # Feature Extracting
    model = load_model(model_name='resnet101',
                       image_size=image_size,
                       )
    img_names, img_vectors = model.extract_feature_vectors(dataset_path=dataset_path,
                                                           )
    # images_path = [dataset_path + '/' + img_names[i] for i in range(len(img_names))]
    print(" > Making Feature Vectors is Done!")
    print()

    # elastic_search_by_vector(focus_index, img_vectors)


# test-case for a data with K=10
# start_time = time.time()
# s = "T1661T1661T1661T1661T1661T1661T1661T1661T1661T1661 T1065T1065T1065T1065T1065T1065T1065T1065T1065 T1335T1335T1335T1335T1335T1335T1335T1335 T715T715T715T715T715T715T715 T1751T1751T1751T1751T1751T1751 T385T385T385T385T385 T869T869T869T869 T343T343T343 T508T508 T311"
# f_index = 'data'
# elastic_searching(f_index, s)
# end_time = time.time()
# duration = end_time - start_time
# print("The code took", duration, "seconds to execute.")


path = 'dataloading/Selected dataset'
elastic_search_by_image('esm', path)
