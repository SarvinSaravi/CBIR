from feature_extraction import feature_extracting
from similarity import load_similarity
from crelu import load_crelu

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


# from sklearn.metrics.pairwise import cosine_similarity


def main():
    threshold = 0.65
    dataset_path = "Selected_dataset"
    img_names, img_vectors = feature_extracting(dataset_path)
    print(" > Making Feature Vectors is Done!")

    new_vectors = load_crelu(img_vectors)
    print(new_vectors.shape)

    measurement = load_similarity(similarity_name='cosine')

    # Show query
    plt.figure()
    img = mpimg.imread(dataset_path + '/' + img_names[1])
    img_plot = plt.imshow(img)
    plt.show()

    for i in range(len(img_names)):
        result = measurement(img_vectors[1].reshape(1, -1),
                             img_vectors[i].reshape(1, -1),
                             )
        # print(result)
        if result > threshold:
            img = mpimg.imread(dataset_path + '/' + img_names[i])
            img_plot = plt.imshow(img)
            plt.show()
    print(" > Finding similar Images is Done!")


if __name__ == "__main__":
    main()
