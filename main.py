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
from text_representation import load_text_representation


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


def main():
    query = 13
    threshold = 0.65
    k_variable = 400
    dataset_path = "dataloading/Selected dataset"

    img_names, img_vectors = feature_extracting(dataset_path)
    print(" > Making Feature Vectors is Done!")

    crelu_vectors = load_crelu(img_vectors)
    print(crelu_vectors.shape)
    print(" > Making CreLU Vectors is Done!")

    permutation_vectors = np.apply_along_axis(load_permutations, axis=1, arr=crelu_vectors)
    print(permutation_vectors.shape)
    print(" > Making Deep Permutation Vectors is Done!")

    text_strings = np.apply_along_axis(load_text_representation, axis=1, arr=permutation_vectors, k=k_variable)
    print(text_strings.shape)
    print(" > Making STR is Done!")

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
