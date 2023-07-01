import numpy as np
# from reports.save_in_files import save_in_npz
import csv
import time

from models import load_model
from crelu import load_crelu
from permutation_text import vector2text_processing
from partitioning import partitioning_process
from elastic import elastic_indexing_with_titles, elastic_search_by_vector


# from dataloading import dataloading as dl


def main():
    # Initialize
    start_time = time.time()
    query = 10
    threshold = 0.7
    K = 42  # text representation
    num_sections = 100  # that every part will be (50,40) OR (50,41)
    # or L
    L = 11
    dataset_path = "dataloading/Selected dataset"
    image_size = (224, 224)

    # Feature Extracting
    model = load_model(model_name='resnet101',
                       image_size=image_size,
                       )
    img_names, img_vectors = model.extract_feature_vectors(dataset_path=dataset_path,
                                                           )
    images_path = [dataset_path + '/' + img_names[i] for i in range(len(img_names))]
    print(" > Making Feature Vectors is Done!")

    # Making CReLU Vectors
    crelu_vectors = load_crelu(img_vectors)
    print(crelu_vectors.shape)
    print(" > Making CreLU Vectors is Done!")

    """ *> string_list should be indexed in ElasticSearch """
    string_list = vector2text_processing(crelu_vectors, K)
    print("| string list length | = " + str(len(string_list)))

    """
        Partitioning Process
        *> part_k is a parameter same as k but for every part of partitions
        *> num_sections is the number of partitions that vectors divided into
        *> L is the Length of every partition that vectors divided into
        *> partition_string_list should be indexed in ElasticSearch
    """
    # print(" > Process of partitioning!")
    # partition_string_list = partitioning_process(crelu_vectors, part_k=5, length=L)
    # partition_string_list = partitioning_process(crelu_vectors, part_k=20, num_sec=num_sections)

    # Save output
    # hyperparams = {'query': query, 'threshold': threshold, 'K': K, 'S': num_sections, 'image_size': image_size}
    # save_in_npz(data=img_vectors,
    #             hyperparams=hyperparams,
    #             file_name="S",
    #             )

    # save/index(string_list) into Elasticsearch
    index_name = 'title_data_k%s' % K
    elastic_indexing_with_titles(img_names, string_list, K, focus_index=index_name,
                                 shard_number=1,
                                 replica_number=0)
    print(" > Indexing data in Elasticsearch is Done!")

    # search and compare pictures together
    result = np.zeros(2500).reshape(50, 50)

    for i in range(len(img_names)):
        query_vector = img_vectors[i]
        search_answer = elastic_search_by_vector(index_name, query_vector, K)
        for id, score in search_answer.items():
            id = int(id)
            result[i][id - 1] = score

    # save output
    filename = 'result_K%s.csv' % K
    np.savetxt("results/csv/" + filename, result, delimiter=',', fmt='%s')
    print(" > Searching in Elasticsearch is Done And Results saved in ", filename)

    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print("The code took %s seconds to execute with K = %s" % (duration, K))


if __name__ == "__main__":
    main()
