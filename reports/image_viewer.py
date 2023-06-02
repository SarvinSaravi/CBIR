import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import numpy as np
import pandas as pd

def show_image(image,
               title="",
               ):
    plt.imshow(image)
    plt.title(title, fontsize=18)
    plt.axis('off')
    plt.show()


def show_image_from_path(image_path,
                         title="",
                         ):
    img = mpimg.imread(image_path)
    show_image(img, title)


def show_images_from_path(images_path,
                          title="Image",
                          ):
    for i, img_path in enumerate(images_path):
        show_image_from_path(img_path, title + " " + str(i))


def test_visualize(data, label_list):

    data = pd.DataFrame(data)
    corr = data.corr()
    sns.heatmap(corr, cmap='coolwarm')
    plt.title('Correlation heatmap')
    plt.show()

    sns.pairplot(data)
    return
