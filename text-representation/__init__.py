from .text import generate_txt_truncate


def load_text_representation(permutation_vector, k, **kwargs):
    """
        Get text generation

        the permutation vector must be a vector of Integers

    """
    return generate_txt_truncate(permutation_vector, k)
