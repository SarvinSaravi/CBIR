from .deep_permutation import generate_permutation
from .text import generate_text_opt, generate_text_with_separator
import numpy as np


def vector2text_processing(base_vector, K):
    """
        base_vector can be used in 2 way:
            1) one d-dimensional vector
            2) multiple vectors in shape of ndarray

        K is a parameter for truncate text representation
    """
    permutation_vectors = np.apply_along_axis(generate_permutation, axis=1, arr=base_vector)
    # print(permutation_vectors.shape)
    # print(" > Making Deep Permutation Vectors is Done!")

    texts = list(generate_text_opt(item, K) for item in permutation_vectors)
    # print(len(texts))
    # print(" > Making Surrogate Text Representation is Done!")

    return texts


def vector2text_processing_with_splitter(base_vector, K):
    """
        base_vector can be used in 2 way:
            1) one d-dimensional vector
            2) multiple vectors in shape of ndarray

        K is a parameter for truncate text representation
    """
    permutation_vectors = np.apply_along_axis(generate_permutation, axis=1, arr=base_vector)
    # print(permutation_vectors.shape)
    # print(" > Making Deep Permutation Vectors is Done!")

    texts = list(generate_text_with_separator(item, K) for item in permutation_vectors)
    # print(len(texts))
    # print(" > Making Surrogate Text Representation with space splitter is Done!")

    return texts
