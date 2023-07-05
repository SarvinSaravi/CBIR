import time
import numpy as np

from dataloading.dataloading import loading_from_npz
from elastic import elastic_search_idea3


def search_results():
    # Initialize
    K = 42
    index_name = 'title_data_k%s' % K
    # Loading features
    data = dict(loading_from_npz(file_name="Selected dataset_features.npz"))
    img_names, img_vectors = np.array(list(data.keys())), np.array(list(data.values()))

    start_time = time.time()
    # search and compare pictures together
    result = np.zeros(2500).reshape(50, 50)

    for i in range(len(img_names)):
        query_vector = img_vectors[i]
        search_answer = elastic_search_idea3(index_name, query_vector, K)
        for ans_id, ans_score in search_answer.items():
            ans_id = int(ans_id)
            result[i][ans_id - 1] = ans_score

    # save output
    filename = 'result_K%s.csv' % K
    np.savetxt("results/csv/" + filename, result, delimiter=',', fmt='%s')
    print(" > Searching in Elasticsearch is Done And Results saved in ", filename)

    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print("The code took %s seconds to execute with K = %s" % (duration, K))

    print()


if __name__ == '__main__':
    search_results()
