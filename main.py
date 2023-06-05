import numpy as np
from reports.save_in_files import save_in_npz

from models import load_model
from crelu import load_crelu
# from permutation import load_permutations
# from text_representation import load_text_representation
from permutation_text import vector2text_processing


def partitioning(base_vector, num_sec, part_k=4):
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
    K = 400  # text representation
    num_sections = 100  # that every part will be (50,40) OR (50,41)
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

    """ *> string_list should be indexed in ElasticSearch """
    string_list = vector2text_processing(crelu_vectors, K)
    # print(len(string_list))
    # print(string_list[0])

    """
        Partitioning Process
        *> part_k is a parameter same as k but for every part of partitions
        *> num_sections is the number of partitions that vectors divided into
        *> partition_string_list should be indexed in ElasticSearch
    """
    print(" > Process of partitioning!")
    partition_string_list = partitioning(crelu_vectors, num_sections, part_k=20)
    print(len(partition_string_list))
    print(partition_string_list[0])

    # Save output
    hyperparams = {'query': query, 'threshold': threshold, 'K': K, 'S': num_sections, 'image_size': image_size}
    save_in_npz(data=img_vectors,
                hyperparams=hyperparams,
                file_name="S",
                )


if __name__ == "__main__":
    main()
