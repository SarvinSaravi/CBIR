import numpy as np
from permutation_text import vector2text_processing_with_splitter


def partitioning_by_number_segments(base_vector, num_sec, part_k=4):
    """
        return type of next function is a list and each element is a 2d Numpy array
        (the same number of vectors in truncated dimensions)
    """
    partition_list = np.array_split(base_vector, num_sec, axis=1)
    # print(" > Split array to partitions is Done!")
    # print(f" > The output is ( {len(partition_list)}, {partition_list[0].shape[0]}, {partition_list[0].shape[1]})")
    # print(partition_list)

    string_list = []

    for part in partition_list:
        """ a list format """
        text_strings = vector2text_processing_with_splitter(part, part_k)
        string_list.append(text_strings)

    # print(" > Creating text string for partitions is Done!")
    return string_list


def partitioning_by_length(base_vector, length, part_k=4):
    dimension = base_vector.shape[1]
    num_sec = dimension // length + (dimension % length != 0)
    num_padded_zero = num_sec * length - dimension
    padded_vector = np.pad(base_vector, ((0, 0), (num_padded_zero, 0)), mode='constant')

    return partitioning_by_number_segments(padded_vector, num_sec, part_k)
