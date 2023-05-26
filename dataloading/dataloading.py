import keras.utils as ut

import os


"""
Notes
__________
    path means direction to the file/folder + the file/folder name
    dir means only direction to the file/folder
"""
def loading_an_image(img_path, image_size):
    """This function loads an image.
    """
    img = ut.load_img(img_path,
                      target_size=image_size,
                      )
    return img


def loading_image_dataset(dataset_path,
                          image_size=(224, 224),
                          ) -> dict:
    """This function laods a list of images in a given folder path.
    """
    image_list = dict()  # key: image name, val: image
    all_img_names = os.listdir(dataset_path)
    for img_name in all_img_names:
        image_path = dataset_path + '/' + img_name
        img = loading_an_image(image_path, image_size)
        image_list[img_name] = img
        print(" > Loading Images is Done!")
    return image_list
