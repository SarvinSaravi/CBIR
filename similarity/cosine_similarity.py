from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def cosine(dataset_path,
           feature_vectors: dict,
           threshold: float = 0.65,
           ):
    img_names = feature_vectors.keys()
    # Show query
    img = mpimg.imread(dataset_path + img_names[1162])
    img_plot = plt.imshow(img)
    plt.show()
    for i in range(len(img_names)):
        measurement = cosine_similarity(feature_vectors[img_names[1162]].reshape(1, -1),
                                        feature_vectors[img_names[i]].reshape(1, -1),
                                        )
        if measurement > threshold:
            img = mpimg.imread(dataset_path + img_names[i])
            img_plot = plt.imshow(img)
            plt.show()
