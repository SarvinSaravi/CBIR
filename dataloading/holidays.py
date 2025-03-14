import os
import tarfile
import shutil
import zipfile

class Holidays:
    def __init__(self,
                 dataset_folder="results/holidays",   # where all data about the dataset are kept
                 batch_size=1491,
                 archive_files=[f"data/holidays/jpg{i}.tar.gz" for i in range(1,3)], # source dataset files {.zip, .tar.gz}
                 chunk=False, # True, if chunk the data based on batch_sizem False if all images in a single folder
                 verbose=False,
                 ) -> None:
        
        self.dataset_name="holidays"
        self.dataset_folder=dataset_folder
        self.dataset_path=f"{dataset_folder}/images" # where all images goes.
        self.dataset_size = 1491
        self.batch_size = batch_size
        self.archive_files = archive_files
        self.chunk = chunk
        self.verbose = verbose

        self.num_batches=self.dataset_size // batch_size + (self.dataset_size % batch_size != 0)
        
    def prepare(self, start_img_idx=0):

        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path)
        if self.verbose:
                print(" > Archive files:\n", self.archive_files)

        temp = f"{self.dataset_folder}/tmp"

        img_idx = start_img_idx
        batch_index = start_img_idx // self.batch_size
        batch_path = f"{self.dataset_path}/{batch_index}"
        
        # Unzip
        for archive in self.archive_files:
            os.makedirs(temp)
            if archive.endswith(".zip"):
                with zipfile.ZipFile(archive, 'r') as zip:
                    zip.extractall(temp)
                    zip.close()
            elif archive.endswith('.tar.gz'):
                with tarfile.open(archive, "r:gz") as tar:
                    tar.extractall(temp)
                    tar.close()
            if self.verbose:
                print(f" > Extracting {archive} complete!")

            if not self.chunk:
                for root, dirs, files in os.walk(temp):
                    for file in files:
                        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            img_path = os.path.join(root, file)
                            shutil.move(img_path, self.dataset_path)
                if self.verbose:
                    print(f" > The {archive} is moved without chunking!")

            else:
                if not os.path.exists(batch_path):
                    os.makedirs(batch_path)
                for root, dirs, files in os.walk(temp):
                    for file in files:
                        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            if img_idx == (batch_index + 1 ) * self.batch_size:
                                batch_index += 1
                                batch_path = f"{self.dataset_path}/{batch_index}"
                                os.makedirs(batch_path)
                            
                            img_path = os.path.join(root, file)
                            shutil.move(img_path, batch_path)
                            img_idx += 1
                if self.verbose:
                    print(f" > The {archive} is chunked!")
                            
            shutil.rmtree(temp)                    

        if self.verbose:
            print(f" > Preparing {self.dataset_name} dataset complete!")
    
    def access_dataset(self):
        if self.chunk:
            return [f"{self.dataset_path}/{batch_index}" for batch_index in range(self.num_batches)]
        else:
            return [self.dataset_path, ]
