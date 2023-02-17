from feature_extraction import feature_extracting
from similarity import load_similarity


def main():
    dataset_path = ""
    img_vectors = feature_extracting(dataset_path)
    load_similarity(similarity_name='cosine',
                    dataset_path=dataset_path,
                    feature_vectors=img_vectors,
                    threshold=0.65,
                    )


if __name__ == "__main__":
    main()
