import time
import os

from models import load_model
from dataloading import load_dataset
from reports.save_in_files import save_in_npz
from dataloading.dataloading import loading_an_image
from dataloading.dataset import prepare_dataset

def extract_features_batch_vectors(img_names,
                                   folder_path,
                                   model,
                                   img_size,
                                   verbose=False,
                                   ):
    feature_vector = []
    for img_name in img_names:
        img_path = f"{folder_path}/{img_name}" 
        if verbose:
            print(f" > Extracing {img_path} features..!")
        x = loading_an_image(img_path=img_path, 
                             image_size=img_size,
                             )
        x = model.predict(x)
        feature_vector.append(x)
    return feature_vector

def extract_features():
    
    # Initializing ----------------------------------------------------

    # dataset_name can be "holidays", or "mirflickr1m", or "selected"
    dataset_name = "holidays"
    

    model_name = "resnet101"
    rmac = False
    image_size = (224, 224)
    
    verbose = True # Debugging
    # -----------------------------------------------------------------

    # Start timing
    start_time = time.time()
    dataset = load_dataset(dataset_name=dataset_name,
                           verbose=verbose,
                           )
    dataset.prepare() # to chunk or prepare images from source (.zip) files 

    model = load_model(model_name=model_name,
                       image_size=image_size,
                       rmac=rmac,
                       verbose=False,
                       )
   

    features_vectors = []
    img_names = []
    path_list = dataset.access_dataset()

    for folder_path in path_list:
        if not os.path.exists(folder_path):
            print(f" > {folder_path} is not existed!")
            continue

        img_names = [img_name for img_name in os.listdir(folder_path)]
        
        feature_vectors = extract_features_batch_vectors(img_names=img_names,
                                                         folder_path=folder_path,
                                                         model=model,
                                                         img_size=image_size,
                                                         verbose=verbose,
                                                        )
        
        # save features batch vectors
        file_name = f"feature_vectors"
        save_in_npz(data=dict(zip(img_names, feature_vectors)),
                    file_name=file_name,
                    file_dir=folder_path,
                    )
        # os.system('cls')  # clear terminal
        print(f" > Making Feature Vectors for {folder_path} is Done!")

    end_time = time.time()
    duration = end_time - start_time

    print(" > The feature extracting took %s seconds." % duration)

if __name__ == "__main__":
    extract_features()
