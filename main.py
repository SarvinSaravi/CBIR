import numpy as np
from keras.applications.resnet import preprocess_input
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import os

from dataloading.dataloading import loading_image_dataset
from models import load_model
from similarity import load_similarity
from crelu import load_crelu
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


def partitioning(base_vector, num_sec, part_k=5):
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
    query = 13
    threshold = 0.65
    k = 400
    dataset_path = "dataloading/Selected dataset"

    img_names, img_vectors = feature_extracting(dataset_path)
    print(" > Making Feature Vectors is Done!")

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

    measurement = load_similarity(similarity_name='cosine')

    # Show query
    plt.figure()
    img = mpimg.imread(dataset_path + '/' + img_names[query])
    img_plot = plt.imshow(img)
    plt.show()

    for i in range(len(img_names)):
        result = measurement(img_vectors[query].reshape(1, -1),
                             img_vectors[i].reshape(1, -1),
                             )

        if result > threshold:
            print(result)
            img = mpimg.imread(dataset_path + '/' + img_names[i])
            img_plot = plt.imshow(img)
            plt.show()
    print(" > Finding similar Images is Done!")


if __name__ == "__main__":
    main()
