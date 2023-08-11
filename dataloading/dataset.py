import os
import tarfile
import shutil
import zipfile
from dataloading.mirflickr1m import Mirflickr1m
def find_images():
# find all jpg and move to dataset_path
    for root, dirs, files in os.walk(temp):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(root, file)
                shutil.move(img_path, dataset_path)
    return

# def move_folders(source, dest):
    
#     folders = [folder for folder in os.listdir(source) if os.path.isdir(os.path.join(source, folder))]
#     for folder in folders:
#           source_path = os.path.join(source, folder)
#           dest_path = os.path.join(dest, folder)
#           shutil.move(source_path, dest_path)
#     return

# def prepare(dataset_name, dataset_folder, dataset_size, batch_size, archive_files, chunk, verbose):

#     num_batch = dataset_size // batch_size + (dataset_size % batch_size != 0)
    
#     dataset_path = f"{dataset_folder}/images"
#     if not os.path.exists(dataset_path):
#         os.makedirs(dataset_path)
#         if verbose:
#                 print(" > Archive files:\n", archive_files)

#         temp = dataset_folder +"/tmp"
#         # Unzip
#         for archive in archive_files:
#             os.makedirs(temp)
#             if archive.endswith(".zip"):
#                 with zipfile.ZipFile(archive, 'r') as zip:
#                     zip.extractall(temp)
#                     zip.close()
#             elif archive.endswith('.tar.gz'):
#                 with tarfile.open(archive, "r:gz") as tar:
#                     tar.extractall(temp)
#                     tar.close()
#             if verbose:
#                 print(f" > Extracting {archive} complete!")

#             if dataset_name == "mirflickr1m" and batch_size == 10000:
#                 move_folders(f"{temp}/images", dataset_path)
#                 if verbose:
#                      print(f" > The {dataset_name} dataset is moved to {dataset_path}!")
#             else:
#                 # remove any .txt files
#                 files = os.listdir(dataset_folder)
#                 for file in files:
#                     if file.endswith(".txt"):
#                         file_path = os.path.join(dataset_folder, file)
#                         os.remove(file_path)
#                 if verbose:
#                         print(f" > Removing .txt file complete!")
            
#                 img_idx = 0
#                 files = os.listdir(dataset_path)
#                 files.sort()
#                 for batch_index in range(num_batch):
#                     file_path = f"{dataset_folder}/batch{batch_index}.txt"
#                     with open(file_path, 'w') as f:
#                         while img_idx < (batch_index + 1 ) * batch_size:
#                             # img_path = os.path.join(dataset_path, files[img_idx])
#                             f.write(files[img_idx] + '\n')
#                             img_idx += 1
#                         f.close()
#                     if verbose:
#                             print(f" > Writing {file_path} complete!")
                
                
#                 shutil.rmtree(temp)
    
#     return num_batch
    
def prepare_dataset(dataset_name, 
                    batch_size, 
                    source_dir="data",
                    chunk=True,
                    verbose = False):
    
    dataset = Mirflickr1m(batch_size=batch_size, verbose=verbose)
    dataset.prepare()
    return dataset
    # archive_files = []
    # dataset_size = 0
    # if dataset_name == "holidays":
    #     print(f" > Preparing {dataset_name} dataset...")
    #     dataset_folder = "results/holidays"
    #     dataset_size = 1419
    #     archive_files = [f"{source_dir}\holidays\jpg{i}.tar.gz" for i in range(1,3)]
    # elif dataset_name == "mirflickr1m":
        
    # elif dataset_name == "selected":
    #     print(f" > Preparing {dataset_name} dataset...")
    #     dataset_folder = "results/selected"
    #     dataset_size = 50
    #     archive_files = [f"{source_dir}\selected\selected.zip"]
    # else:
    #      print(f" > The {dataset_name} dataset is not found!")
         

    # num_batch = prepare(dataset_name=dataset_name,
    #                     dataset_folder=dataset_folder,
    #                     dataset_size=dataset_size,
    #                     batch_size=batch_size,
    #                     archive_files=archive_files,
    #                     chunk=chunk,
    #                     verbose=verbose
    #                     )
    # print(f" > Preparing {dataset_name} dataset with batch_size {batch_size} is Done!")
    return num_batch
