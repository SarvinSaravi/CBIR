from dataloading.dataloading import loading_from_npz
import numpy as np
# from reports.save_in_files import save_in_json
import time
from crelu import load_crelu
# from permutation_text import vector2text_processing_with_splitter
from partitioning import partitioning_process
from elastic import elastic_indexing


def encode_features():
    # initiate
    # K = 42
    indexing_mechanism = 'partitioning'

    num_sections = 10
    partition_K = 42
    K = partition_K

    start_time = time.time()
    # Loading features
    data = dict(loading_from_npz(file_dir="results/npz/Mirflickr1m/99", file_name="feature_vectors.npz"))
    # data = dict(loading_from_npz(file_name="Main dataset_features.npz"))
    img_names, img_vectors = np.array(list(data.keys())), np.array(list(data.values()))

    img_vectors = img_vectors.reshape(10000, 2048)

    # Making CReLU Vectors
    crelu_vectors = load_crelu(img_vectors)
    print(crelu_vectors.shape)
    print(" > Making CreLU Vectors is Done!")

    """ *> string_list should be indexed in ElasticSearch """
    # string_list = vector2text_processing_with_splitter(crelu_vectors, K)
    # print(" > Making Strings from vectors is Done!")
    # print("| string list length | = " + str(len(string_list)))

    """
        Partitioning Process
        *> part_k is a parameter same as k but for every part of partitions
        *> num_sections is the number of partitions that vectors divided into
        *> L is the Length of every partition that vectors divided into
        *> partition_string_list should be indexed in ElasticSearch
    """
    print(" > Process of partitioning!")
    # partition_string_list = partitioning_process(crelu_vectors, part_k=5, length=L)
    partition_string_list = partitioning_process(crelu_vectors, part_k=partition_K, num_sec=num_sections)
    print(" >  The partitioning procedure is complete and the number of partitions is : ", len(partition_string_list))

    # save output of encoded features
    # file_name = "data_encoded_data_k%s" % K
    # file_path = 'results/json/Flickr1M/partitioning/0'
    # save_in_json(data=(img_names, partition_string_list),
    #              file_name=file_name,
    #              file_dir=file_path
    #              )

    # save/index(string_list) into Elasticsearch
    # index_name = 'm_title_data_k%s' % K
    index_name = indexing_mechanism + '_title_data_k%s' % K
    elastic_indexing(img_names, partition_string_list, index_name, indexing_method=indexing_mechanism)
    print(" > Indexing data in Elasticsearch with method %s is Done!" % indexing_mechanism)
    # print("| Elasticsearch Index Name | = " + index_name)

    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print("Encoding and Indexing features took %s seconds to execute with K = %s" % (duration, K))
    return


if __name__ == "__main__":
    encode_features()
