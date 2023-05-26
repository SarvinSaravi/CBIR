
from keras.applications import ResNet101
from keras import Sequential, Model
from keras.layers import Lambda, Input
from keras.applications.resnet import preprocess_input

class Resnet101:
    def __init__(self,
                 image_size: tuple,
                 n_classes: int,
                 ):
        self.input_shape = image_size + (3,)
        self.n_classes = n_classes

    def get_model(self) -> Model:
        model = ResNet101(#include_top=False,
                         input_shape=self.input_shape,
                         # pooling='avg',
                         weights='weights/resnet101_weights_tf_dim_ordering_tf_kernels.h5',
                         )

        final_model = Sequential()
        final_model.add(Lambda(preprocess_input,
                               input_shape=self.input_shape))
        final_model.add(model)

        # print(model.summary())
        return final_model
