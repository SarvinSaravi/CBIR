from keras.applications import ResNet50
from keras import Sequential, Model
from keras.layers import Lambda, Input
from keras.applications.resnet import preprocess_input
import numpy as np

from dataloading.dataloading import loading_image_dataset

class Resnet50:
    def __init__(self,
                 image_size: tuple,
                 ):
        self.image_size = image_size
        self.input_shape = image_size + (3,)
        self.model = None
        return

    def get_model(self):
        base_model = ResNet50(include_top=False,
                              input_shape=self.input_shape,
                              pooling='avg',
                              weights='weights/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
                              )

        model = Sequential()
        model.add(Lambda(preprocess_input,
                         input_shape=self.input_shape))
        model.add(base_model)
        # print(model.summary())
        self.model = model
        return self

    def extract_feature_vectors(self,
                                dataset_path):
        images_dict = loading_image_dataset(dataset_path,
                                            self.image_size,
                                            )
        image_names = list(images_dict.keys())
        image_list = list(images_dict.values())

        img_vectors = self.model.predict(np.vstack(image_list))
        print(img_vectors.shape)

        return image_names, img_vectors