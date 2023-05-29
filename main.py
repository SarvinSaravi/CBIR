import numpy as np


from dataloading.dataloading import loading_image_dataset
from models import load_model
from crelu import load_crelu
from permutation import load_permutations
from reports.search_via_query import *
from similarity.bm25_similarity import bm25
def generate_text(vector, k):
    text_vector = []
    for i in range(1, k + 1):
        v = vector[i - 1]
        Ti = "T" + str(i)
        rep = (k + 1) - v
        text_vector.append(Ti * rep)

    text_vector.sort(key=len, reverse=True)
    text = ''.join(text_vector)
    # print(text)
    return text

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
    query = 10
    threshold = 0.50
    k = 400
    dataset_path = "dataloading/Selected dataset"

    img_names, img_vectors = feature_extracting(dataset_path)
    print(" > Making Feature Vectors is Done!")
    images_path = [dataset_path + '/' + img_names[i] for i in range(len(img_names))]
    search_via_query(query_path=dataset_path + '/' + img_names[query],
                     images_path=images_path,
                     query_vector=img_vectors[query],
                     img_vectors=img_vectors,
                     threshold=threshold,
                     )

    crelu_vectors = load_crelu(img_vectors)
    print(crelu_vectors.shape)
    print(" > Making CreLU Vectors is Done!")

    permutation_vectors = np.apply_along_axis(load_permutations, axis=1, arr=crelu_vectors)
    print(permutation_vectors.shape)
    print(" > Making Deep Permutation Vectors is Done!")

    text_vectors = list()
    for vector in permutation_vectors:
        text_vectors.append(generate_text(vector, k))
    scores = bm25(text_vectors[query], text_vectors)
    similar_images = compare_with_threshold(scores, threshold)
    show_search_results(images_path[query],
                        images_path,
                        similar_images)



if __name__ == "__main__":
    main()
