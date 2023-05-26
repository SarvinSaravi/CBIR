from .text import generate_text_opt


def load_text_representation(permutation_vector, k, **kwargs):
    """
        Get text generation

        the permutation vector must be a vector of Integers

    """
    return generate_text_opt(permutation_vector, k)
