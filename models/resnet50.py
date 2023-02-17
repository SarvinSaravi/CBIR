
from keras.applications import ResNet50
from keras import Sequential, Model
from keras.layers import Dense, Input


class Resnet50:
    def __init__(self,
                 image_size: tuple,
                 n_classes: int,
                 ):
        self.input_shape = image_size + (3,)
        self.n_classes = n_classes

    def get_model(self) -> Model:
        data_input = Input(self.input_shape)
        model = ResNet50(#include_top=False,
                         input_shape=self.input_shape,
                         # pooling='avg',
                         weights='weights/resnet50_weights_tf_dim_ordering_tf_kernels.h5',
                         )

        # model = Sequential()
        # model.add(ResNet50(include_top=False, pooling='avg', weights='weights/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'))

        # last layer for two classes
        # model.add(Dense(self.n_classes, activation='softmax'))

        # trainable
        # model.layers[0].trainable = False
        final_model = Model(model.input, model.layers[-2].output)
        # print(model.summary())
        return final_model
