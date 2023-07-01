# Visual Search

 Dataset Link [Link](visual-search/dataloading)


`extract_features.py` 

Image Dataset -> list of features vectors (narrays of narrays)

1. It extracts features from Selected dataset.
2. It saves results into selected dataset_features.npz.



`encode_features.py`

list of features vectors (narrays of narrays) -> list of texts ( list of strings: N * D or/ S * N * D)

1. It encodes features vectors into strings.
2. It saves results of encoded features into selected dataset_encoded_features.csv.
3. It indexes the list of text into elastic.