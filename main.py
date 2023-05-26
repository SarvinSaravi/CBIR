from feature_extraction import feature_extracting
from similarity import load_similarity

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity


def main():
    query = 9
    threshold = 0.7
    dataset_path = "dataloading/Selected dataset"
    # dataset_path = "Flicker8k_Dataset"
    img_names, img_vectors = feature_extracting(dataset_path)
    print(" > Making Feature Vectors is Done!")
    mesurement = load_similarity(similarity_name='cosine')

    # Show query
    plt.figure()
    img = mpimg.imread(dataset_path + '/' + img_names[query])
    img_plot = plt.imshow(img)
    plt.show()

    for i in range(len(img_names)):
        result = mesurement(img_vectors[query].reshape(1, -1),
                            img_vectors[i].reshape(1, -1),
                            )
        # print(result)

        if result > threshold:
            print(result)
            img = mpimg.imread(dataset_path + '/' + img_names[i])
            img_plot = plt.imshow(img)
            plt.show()
    print(" > Finding similar Images is Done!")


if __name__ == "__main__":
    main()
