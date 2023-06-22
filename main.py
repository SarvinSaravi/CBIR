# import numpy as np
# from reports.save_in_files import save_in_npz
import csv

from models import load_model
from crelu import load_crelu
from permutation_text import vector2text_processing
from partitioning import partitioning_process
from elastic import elastic_indexing, elastic_searching


# from dataloading import dataloading as dl


def main():
    # Initialize
    query = 10
    threshold = 0.7
    K = 400  # text representation
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

    # *> string_list should be indexed in ElasticSearch
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

    elastic_indexing(string_list, K, focus_index='data2', shard_number=5, replica_number=0)


if __name__ == "__main__":
    main()
