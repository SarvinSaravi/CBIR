import numpy as np
import time
from models import load_model
from reports.save_in_files import save_in_csv
from dataloading.dataloading import loading_from_csv

# from dataloading import dataloading as dl


def extract_features():
    # Start timing
    start_time = time.time()
    dataset_name = "Selected dataset"
    dataset_path = "dataloading/Selected dataset"
    image_size = (224, 224)
    model_name = "resnet101"

    model = load_model(model_name=model_name,
                       image_size=image_size,
                       )
    img_names, img_vectors = model.extract_feature_vectors(dataset_path=dataset_path,
                                                           )
    images_path = [dataset_path + '/' + img_names[i] for i in range(len(img_names))]

    # save output
    file_name = dataset_name + "_features"
    save_in_csv(data=(img_names, img_vectors),
                file_name=file_name,
                )
    print(" > Making Feature Vectors is Done And Results saved in %s." % file_name)

    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print(" > The feature extracting took %s seconds." % duration)


if __name__ == "__main__":
    extract_features()

