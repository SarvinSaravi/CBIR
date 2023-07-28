import time
import numpy as np

from dataloading.dataloading import loading_from_npz
from elastic import elastic_search_by_vector
from evaluation.evaluation_functions import get_queries, result_assessment


def search_results():
    # Initialize
    K = 42
    # index_name = 'm_title_data_k%s' % K
    searching_mechanism = 'prefix_search'
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


if __name__ == '__main__':
    search_results()
