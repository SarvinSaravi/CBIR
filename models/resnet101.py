from keras.applications import ResNet101
from keras import Sequential, Model
from keras.layers import Lambda, Input
from keras.applications.resnet import preprocess_input
import numpy as np

from dataloading.dataloading import loading_image_dataset, loading_an_image
from models.rmac import RMAC

class Resnet101:
    def __init__(self,
                 image_size: tuple,
                 rmac=True,
                 verbose=False,
                 ):
        self.image_size = image_size
        self.input_shape = image_size + (3,)
        self.rmac = rmac
        self.model = None
        self.verbose = verbose
        return

    def get_model(self,
                  ):
        base_model = ResNet101(include_top=False,
                               input_shape=self.input_shape,
                               pooling='avg',
                               weights='data/weights/resnet101_weights_tf_dim_ordering_tf_kernels_notop.h5',
                               )
        
        if self.rmac:
            layer = "conv5_block3_out"
            base_out = base_model.get_layer(layer).output
            rmac = RMAC(base_out.shape,
                        scales=5,  # scales at which to generate pooling regions
                        power= None,  # power exponent to apply (not used by default)
                        norm_fm=True,  # normalize feature maps
                        sum_fm=True,  # sum feature maps
                        verbose=False,  # shows details about the regions used
                        )
            rmac_layer = Lambda(rmac.rmac, input_shape=base_model.output_shape, name="rmac_" + layer)
            out = rmac_layer(base_out)
            # out = Dense(2048)(out) # fc to desired dimensionality
            model = Model(base_model.input, out)
            print(" > Creating Resnet101 model with RMAC layer is Done.")
        else:
            model = base_model
            print(" > Creating Resnet101 model is Done.")

        # print(model.summary())
        self.model = model
        return self
    
    def predict(self,x):
        x = preprocess_input(x)
        x = self.model.predict(x, verbose=self.verbose)
        return x
    
