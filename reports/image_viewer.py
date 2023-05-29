import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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
