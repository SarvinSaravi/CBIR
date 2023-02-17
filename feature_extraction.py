from models import load_model

import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.application import ResNet50

img_vectors = dict()
def preprocess_image(img):
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = ResNet50.preprocess_input(img)
    return img


def feature_extracting_img(img_path) -> None:

    img = image.load_img(img_path,
                         # target_size= image_size,
                         )
    input = preprocess_image(img)
    model = load_model(model_name='resnet50',
                       image_size=(224, 224),
                       n_classes=2,
                       )

    predicted_y = model.predict(input)
    predicted_y = np.reshape(predicted_y, predicted_y.shape[1])
    img_vectors[img] = predicted_y


def feature_extracting(dataset_path):
    for img_path in all_img_paths:
        feature_extracting_img(img_path=img_path)
    feature_extracting_img(query_path)
    return img_vectors

