from dataloading.dataloading import loading_from_csv

def encode_features():
    # load features
    data = loading_from_csv(file_name="Selected dataset_features.csv")
    img_names, img_vectors = [row[0] for row in data], [row[1] for row in data]



if __name__ == "__main__":
    encode_features()
