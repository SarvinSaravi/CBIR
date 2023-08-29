import os
import time
import numpy as np
import json
import random

from dataloading.dataloading import loading_from_npz
from elastic import elastic_search_by_vector
from evaluation.evaluation_functions import get_queries, result_assessment
from reports.save_in_files import save_in_json


def search_results():
    # Initialize
    K = 42
    # index_name = 'm_title_data_k%s' % K
    searching_mechanism = 'partitioning'
    index_name = searching_mechanism + '_title_data_k%s' % K
    total_time = 0

    # Loading features
    data = dict(loading_from_npz(file_name="Main dataset_features.npz"))
    img_names, img_vectors = np.array(list(data.keys())), np.array(list(data.values()))

    start_time = time.time()

    # start search by get queries from evaluation package
    query_list = get_queries()
    print(" > Loading Queries is Done!")
    result = {}

    # main search flow
    for query in query_list:
        if query in img_names:
            # find the location of the query vector in our structure
            query_name_index = np.where(img_names == query)[0]
            query_vector = img_vectors[query_name_index]
            # search in elastic index (K is for vector to text transformation)
            search_answer, time_taken = elastic_search_by_vector(index_name, query_vector, K,
                                                                 indexing_method=searching_mechanism)
            result[query] = search_answer

            total_time += time_taken

    print(" > Searching in Elasticsearch with method %s is Done!" % searching_mechanism)
    print(" > The Process took %s seconds to search for %s queries" % (total_time / 1000, len(query_list)))
    print(" >>> Average time per query: %s (sec)" % ((total_time / len(query_list)) / 1000))

    # save output and evaluate mAP
    filename = searching_mechanism + '_result_K%s.dat' % K
    result_assessment(result, filename)
    print(" > Results Assessment done and file saved in ", filename)

    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print("The code took %s seconds to execute with K = %s" % (duration, K))


def create_queries():
    # Initialize
    K = 42
    start_time = time.time()

    # Loading queries
    for q_dir in range(10):

        for query in range(100):
            id_number = random.randint(1, 10000)
            file_path = 'results/json/Flickr1M/partitioning/%s/id_%s.json' % (q_dir, id_number)

            with open(file_path) as f:
                data = json.load(f)
                partitions = []

                for key in data.keys():
                    if key != 'title':
                        partitions.append(data[key])

                data_list = [{"match": {"part" + str(i + 1): part_str}} for i, part_str in enumerate(partitions)]

                my_query = {
                    "bool": {
                        "should": data_list, "minimum_should_match": 1
                    }
                }

                # save output of encoded query
                file_name = 'query_id_' + str(id_number)
                file_path = 'results/json/Flickr1M/Queries/%s' % q_dir

                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                save_in_json(data=my_query,
                             file_name=file_name,
                             file_dir=file_path
                             )

                f.close()

    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print("The code took %s seconds to execute with K = %s" % (duration, K))


if __name__ == '__main__':
    # search_results()
    create_queries()
