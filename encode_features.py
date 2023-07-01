from dataloading.dataloading import loading_from_npz
import numpy as np
from reports.save_in_files import save_in_csv
import time
from crelu import load_crelu
from permutation_text import vector2text_processing
from partitioning import partitioning_process
from elastic import elastic_indexing_with_titles, elastic_search_by_vector

def encode_features():
    K = 42

    start_time = time.time()
    # Loading features
    data = dict(loading_from_npz(file_name="Selected dataset_features.npz"))
    img_names, img_vectors = np.array(list(data.keys())), np.array(list(data.values()))

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

    # save output of encoded features
    file_name = "selected data_encoded_features"
    save_in_csv(data=(img_names, string_list),  # each colmun of .csv
                file_name=file_name,
                )

    # save/index(string_list) into Elasticsearch
    index_name = 'title_data_k%s' % K
    elastic_indexing_with_titles(img_names, string_list, K, focus_index=index_name,
                                 shard_number=1,
                                 replica_number=0)
    print(" > Indexing data in Elasticsearch is Done!")

    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print("Encoding features took %s seconds" % duration)
    return


if __name__ == "__main__":
    encode_features()
