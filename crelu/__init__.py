from .crelu_transformation import crelu


def load_crelu(transform_vector, **kwargs):
    """"Get CReLU transformation"""
    return crelu(transform_vector, **kwargs)
