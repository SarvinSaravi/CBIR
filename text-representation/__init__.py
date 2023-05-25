from .text import generate_text


def load_text_representation(permutation_vector, k, **kwargs):
    """
        Get text generation

        the permutation vector must be a vector of Integers

    """
    return generate_text(permutation_vector, k)
