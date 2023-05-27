import numpy as np


def crelu(x):
    """Returns the CReLU activation function applied to the input vector x."""
    relu = np.maximum(0, x)
    neg_relu = np.maximum(0, -x)
    return np.concatenate([relu, neg_relu], axis=-1)
