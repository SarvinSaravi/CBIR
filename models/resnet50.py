
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import Sequential, Model
from tensorflow.keras.layers import Dense, Input


class Resnet50:
    def __init__(self,
                 image_size: tuple,
                 n_classes: int,
                 ):
        self.input_shape = image_size + (3,)
        self.n_classes = n_classes

    def load_model(self) -> Model:

        model = Sequential()
        model.add(Resnet50(include_top=False, pooling='avg', weights='imagenet'))

        # last layer for two classes
        # model.add(Dense(self.n_classes, activation='softmax'))

        # trainable
        model.layers[0].trainable = False

        print(model.summary())
        return model