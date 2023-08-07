import os
import tarfile
import shutil
import zipfile
def prepare(dataset_path, dataset_size, batch_size, archive_files, verbose):

    num_batch = dataset_size // batch_size + (dataset_size % batch_size != 0)
    
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

        
        if verbose:
                print(" > Archive files:\n", archive_files)
        temp = dataset_path +"/tmp"
        # Unzip
        for archive in archive_files:
            os.makedirs(temp)
            if archive.endswith(".zip"):
                with zipfile.ZipFile(archive, 'r') as zip:
                    zip.extractall(temp)
                    zip.close()
            elif archive.endswith('.tar.gz'):
                with tarfile.open(archive, "r:gz") as tar:
                    tar.extractall(temp)
                    tar.close()
            if verbose:
                print(f" > Unzip {archive} complete!")

            # find all jpg and move to dataset_path
            for root, dirs, files in os.walk(temp):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        img_path = os.path.join(root, file)
                        shutil.move(img_path, dataset_path)
            shutil.rmtree(temp)

        print(" > Extracting dataset file complete!")
    else:
        # remove any .txt files
        files = os.listdir(dataset_path)
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(dataset_path, file)
                os.remove(file_path)
        if verbose:
                print(f" > Removing .txt file complete!")
    
    img_idx = 0
    files = os.listdir(dataset_path)
    files.sort()
    for batch_index in range(num_batch):
        file_path = f"{dataset_path}/batch{batch_index}.txt"
        with open(file_path, 'w') as f:
            while img_idx < (batch_index + 1 ) * batch_size:
                # img_path = os.path.join(dataset_path, files[img_idx])
                f.write(files[img_idx] + '\n')
                img_idx += 1
            f.close()
        if verbose:
                print(f" > Writing {file_path} complete!")
    
    return num_batch
    
def prepare_dataset(dataset_name, batch_size, 
                    source_dir="data",
                    verbose = False):
    archive_files = []
    dataset_size = 0
    if dataset_name == "holidays":
        dataset_path = "results/holidays"
        dataset_size = 1419
        archive_files = [f"{source_dir}\holidays\jpg{i}.tar.gz" for i in range(1,3)]
    elif dataset_name == "mirflickr1m":
        dataset_path = "results/mirflickr1m"
        dataset_size = 1000000
        archive_files = [f"{source_dir}\mirflickr1m\images{i}.zip" for i in range(8)]

    num_batch = prepare(dataset_path=dataset_path,
                        dataset_size=dataset_size,
                        batch_size=batch_size,
                        archive_files=archive_files,
                        verbose=verbose
                        )
    print(f" > Preparing {dataset_name} dataset with batch_size {batch_size} is Done!")
    return num_batch
