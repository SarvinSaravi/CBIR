import numpy as np
from keras.applications.resnet import preprocess_input
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import os

from dataloading.dataloading import loading_image_dataset
from models import load_model
from similarity import load_similarity
from crelu import load_crelu
from permutation import load_permutations
from reports.search_vectors_via_query import search_vectors_via_query
from reports.search_texts_via_query import search_texts_via_query
from reports.image_viewer import test_visualize
from reports.pairwise_comparison import compare_pairwise
from text_representation import load_text_representation
# from permutation import load_permutations
# from text_representation import load_text_representation
from permutation_text import vector2text_processing


def feature_extracting(dataset_path,
                       image_size=(224, 224),
                       ) -> (list, list):
    images_dict = loading_image_dataset(dataset_path,
                                        image_size
                                        )
    image_names = list(images_dict.keys())
    image_list = list(images_dict.values())

    model = load_model(model_name='resnet101',
                       image_size=image_size,
                       n_classes=2,
                       )
    print(" > Loading model is Done!")

    img_vectors = model.predict(np.vstack(image_list))
    print(img_vectors.shape)

    return image_names, img_vectors


def partitioning(base_vector, num_sec):
    """
        return type of next function is a list and each element is a 2d Numpy array
        (the same number of vectors in truncated dimensions)
    """
    partition_list = np.array_split(base_vector, num_sec, axis=1)
    print(" > Split array to partitions is Done!")

    string_list = []

    for part in partition_list:
        """ a list format """
        text_strings = vector2text_processing(part, part_k)
        string_list.append(text_strings)

    return string_list


def main():
    # Initialize
    query = 10
    threshold = 0.7
    k = 400  # text representation
    dataset_path = "dataloading/Selected dataset"
    image_size = (224, 224)

    # Feature Extracting
    model = load_model(model_name='resnet101',
                       image_size=image_size,
                       )
    img_names, img_vectors = model.extract_feature_vectors(dataset_path=dataset_path,
                                                           )
    print(" > Making Feature Vectors is Done!")

    # pairwise
    all_scores = compare_pairwise(img_vectors)
    data_list = all_scores
    label_list=['data1']
    test_visualize(data_list, label_list)

    # Validation Vectors
    images_path = [dataset_path + '/' + img_names[i] for i in range(len(img_names))]
    # search_vectors_via_query(query_path=dataset_path + '/' + img_names[query],
    #                          images_path=images_path,
    #                          query_vector=img_vectors[query],
    #                          img_vectors=img_vectors,
    #                          threshold=threshold,
    #                          similarity_func='cosine'
    #                          )

    # Making CReLU Vectors
    crelu_vectors = load_crelu(img_vectors)
    print(crelu_vectors.shape)
    print(" > Making CreLU Vectors is Done!")

    """ *> string_list should be indexed in ElasticSearch """
    string_list = vector2text_processing(crelu_vectors, k)
    # print(len(string_list))
    # print(string_list[0])

    """
        Partitioning Process
        *> part_k is a parameter same as k but for every part of partitions
        *> num_sections is the number of partitions that vectors divided into
        *> partition_string_list should be indexed in ElasticSearch
    """
    print(" > Process of partitioning!")
    num_sections = 100  # that every part will be (50,40) OR (50,41)
    partition_string_list = partitioning(crelu_vectors, num_sections, part_k=20)
    # print(len(partition_string_list))
    # print(partition_string_list[0])

    # Validation Text Strings
    # search_texts_via_query(query_path=images_path[query],
    #                        images_path=images_path,
    #                        query_string=text_strings[query],
    #                        text_strings=text_strings,
    #                        threshold=threshold,
    #                        similarity_func='bm25'
    #                        )


if __name__ == "__main__":
    main()
