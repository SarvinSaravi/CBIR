import time

from models import load_model
from reports.save_in_files import save_in_npz
from dataloading.dataloading import loading_an_image
from dataloading.dataset import prepare_dataset

def extract_features_batch_vectors(img_paths,
                                   model,
                                   img_size,
                                   ):
    
    batch_features = []
    for img_path in img_paths:
        x = loading_an_image(img_path=img_path, 
                             image_size=img_size,
                             )
        x = model.predict(x)
        batch_features.append(x)
    return batch_features

def extract_features():
    
    # Initializing ----------------------------------------------------

    # dataset_name can be "holidays", or "mirflickr1m", or "selected"
    dataset_name = "selected"
    batch_size = 50
    chunk = True
    dataset_folder = f"results/{dataset_name}"

    model_name = "resnet101"
    rmac = False
    image_size = (224, 224)
    
    verbose = True # Debugging
    # -----------------------------------------------------------------

    # Start timing
    start_time = time.time()

    num_batch = prepare_dataset(dataset_name=dataset_name,
                                batch_size=batch_size,
                                chunk=chunk,
                                verbose=verbose,
                                )
    
    if verbose:
        print(f"{dataset_name} dataset with batch size {batch_size}: ")
        print(f"Number of batches: {num_batch}")

    model = load_model(model_name=model_name,
                       image_size=image_size,
                       rmac=rmac,
                       verbose=False,
                       )
   

    features_vectors = []
    img_names = []
    for batch_index in range(num_batch):
        file_path = f"{dataset_folder}/batch{batch_index}.txt"

        with open(file_path, 'r') as file:
            img_batch_names = [line.strip() for line in file.readlines()]
            file.close()
        print("img_batch names :", len(img_batch_names))
        img_batch_paths = [f"{dataset_folder}/images/{img_batch_names[i]}" for i in range(len(img_batch_names))]
    
        features_batch_vectors = extract_features_batch_vectors(img_paths=img_batch_paths,
                                                                model=model,
                                                                img_size=image_size,
                                                                )
        features_vectors.append(features_batch_vectors)
        
        # save features batch vectors
        file_name = f"{dataset_name}_batch{batch_index}_features"
        save_in_npz(data=dict(zip(img_batch_names, features_batch_vectors)),
                    file_name=file_name,
                    )
        print(f" > Making Feature Vectors for batch{batch_index} is Done!")

    # save all features vectors
    # save_in_npz(data=dict(zip(img_names, features_vectors)),
    #                 file_name=f"{dataset_name}_features",
    #                 )
    # time measurement
    end_time = time.time()
    duration = end_time - start_time

    print(" > The feature extracting took %s seconds." % duration)
    return num_batch

if __name__ == "__main__":
    extract_features()
