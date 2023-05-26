from __future__ import division
from __future__ import print_function

from keras.layers import Lambda, Dense, TimeDistributed, Input
from keras.models import Model
from keras.preprocessing import image
from keras.applications import ResNet50
import keras.backend as K

# from models.vgg16 import VGG16
from keras.applications.vgg16 import VGG16
from models.RoiPooling import RoiPooling
# t_regions import rmac_regions, get_size_vgg_feat_map

import scipy.io
import numpy as np
import utils

"""https://github.com/noagarcia/keras_rmac"""



def addition(x):
    sumx = K.sum(x, axis=1)
    return sum


def weighting(input):
    x = input[0]
    w = input[1]
    w = K.repeat_elements(w, 512, axis=-1)
    out = x * w
    return out


def rmac(input_shape, num_rois):

    # Load VGG16
    vgg16_model = VGG16("imagenet", input_shape)
    print('here')
    # Regions as input
    in_roi = Input(shape=(num_rois, 4), name='input_roi')

    # ROI pooling
    x = RoiPooling([1], num_rois)([vgg16_model.layers[-5].output, in_roi])

    # Normalization
    x = Lambda(lambda x: K.l2_normalize(x, axis=2), name='norm1')(x)

    # PCA
    x = TimeDistributed(Dense(512, name='pca',
                              kernel_initializer='identity',
                              bias_initializer='zeros'))(x)

    # Normalization
    x = Lambda(lambda x: K.l2_normalize(x, axis=2), name='pca_norm')(x)

    # Addition
    rmac = Lambda(addition, output_shape=(512,), name='rmac')(x)

    # # Normalization
    rmac_norm = Lambda(lambda x: K.l2_normalize(x, axis=1), name='rmac_norm')(rmac)

    # Define model
    model = Model([vgg16_model.input, in_roi], rmac_norm)

    # Load PCA weights
    mat = scipy.io.loadmat(utils.DATA_DIR + utils.PCA_FILE)
    b = np.squeeze(mat['bias'], axis=1)
    w = np.transpose(mat['weights'])
    model.layers[-4].set_weights([w, b])

    return model




