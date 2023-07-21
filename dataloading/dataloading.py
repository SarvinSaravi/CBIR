import keras.utils as ut
import numpy as np
import csv
import os
import cv2 

"""
Notes
__________
    path means direction to the file/folder + the file/folder name
    dir means only direction to the file/folder
"""


def loading_an_image(img_path):
    """This function loads an image.
    """
    img = cv2.imread(img_path)
    return img


def loading_image_dataset(dataset_path,
                          ) -> dict:
    """This function loads a list of images in a given folder path.
    """
    image_list = dict()  # key: image name, val: image
    all_img_names = os.listdir(dataset_path)
    for img_name in all_img_names:
        image_path = dataset_path + '/' + img_name
        img = loading_an_image(image_path)
        image_list[img_name] = img
    print(" > Loading Images is Done!")
    return image_list


def loading_from_npz(file_dir="results/npz",
                     file_name="",
                     ):
    file_path=file_dir + "/" + file_name
    if not file_path.endswith(".npz"):
        file_path = file_path + ".npz"

    data = np.load(file_path)
    print(" > Loading data from", file_path,"is Done!")
    return data


def loading_from_csv(file_dir="results/csv",
                     file_name="",
                     ):
    file_path = file_dir + "/" + file_name
    if not file_path.endswith(".csv"):
        file_path = file_path + ".csv"

    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    print(" > Loading data form", file_path, "is Done!")
    return data
