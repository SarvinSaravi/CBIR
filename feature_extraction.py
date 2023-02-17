from models import load_model

import os
import numpy as np
import keras.utils as ut
from keras.preprocessing import image
from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input


def preprocessing(img):
    img = ut.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


def loading_images(dataset_path,
                   image_size=(224, 224),
                   ) -> (list, list):
    image_names, image_list = list(), list()
    all_img_paths = os.listdir(dataset_path)
    #tmp = 200
    for img_path in all_img_paths:
        img = ut.load_img(dataset_path + '/' + img_path,
                          target_size=image_size,
                          )
        #if tmp == 0:
            #break
        #tmp -= 1
        x = preprocessing(img)
        image_names.append(img_path)
        image_list.append(x)
    return image_names, image_list


def feature_extracting(dataset_path,
                       image_size=(224, 224),
                       ) -> (list, list):
    image_names, image_list = loading_images(dataset_path=dataset_path)
    print(" > Loading Images is Done!")
    model = load_model(model_name='resnet50',
                       image_size=image_size,
                       n_classes=2,
                       )
    print(" > Loading model is Done!")

    img_vectors = model.predict(np.vstack(image_list))
    print(img_vectors.shape)

    return image_names, img_vectors
