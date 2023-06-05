import keras.utils as ut
import numpy as np

import os

"""
Notes
__________
    path means direction to the file/folder + the file/folder name
    dir means only direction to the file/folder
"""


def loading_an_image(img_path, image_size):
    """This function loads an image and convert to array.
    """
    img = ut.load_img(img_path,
                      target_size=image_size,
                      )
    img = ut.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img


def loading_image_dataset(dataset_path,
                          image_size=(224, 224),
                          ) -> dict:
    """This function loads a list of images in a given folder path.
    """
    image_list = dict()  # key: image name, val: image
    all_img_names = os.listdir(dataset_path)
    for img_name in all_img_names:
        image_path = dataset_path + '/' + img_name
        img = loading_an_image(image_path, image_size)
        image_list[img_name] = img
    print(" > Loading Images is Done!")
    return image_list


def loading_from_npz(file_dir, file_name):
    file_path=file_dir+"/"+file_name+".npz"
    loaded_data = np.load('results.npz')
    data = loaded_data['data']
    hyperparams = loaded_data['hyperparams']
    print(" > Loading data and hyperparams form", file_path,"is Done!")
    return data, hyperparams


def loading_from_csv(file_dir, file_name):
    file_path = file_dir + "/" + file_name + ".csv"
    data = np.genfromtxt(file_path, delimiter=',')
    print(" > Loading data form", file_path, "is Done!")
    return data
