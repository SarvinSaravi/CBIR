
import time
import numpy as np
from dataloading.dataloading import loading_from_npz
from reports.cal_tools import *


def search_vectors_via_query(query_path: str,
                             images_path: list,
                             query_vector,
                             img_vectors,
                             threshold,
                             similarity_func='cosine',
                             ):
    scores = list()
    scores = similarity_check(query_vector,
                              img_vectors,
                              similarity_func,
                              )
    similar_images = compare_with_threshold(scores, threshold)
    show_search_results(query_path,
                        images_path,
                        similar_images,
                        )
    print(" > Finding similar Images via their vectors is Done!")
    return


query = 25
threshold = 0.7
dataset_path = "E:/PycharmProjects/visual-search/dataloading/Selected dataset"
start_time = time.time()
# Loading features
data = dict(loading_from_npz(file_dir="E:/PycharmProjects/visual-search/results/npz",
                             file_name="Selected dataset_features.npz"))
img_names, img_vectors = np.array(list(data.keys())), np.array(list(data.values()))
images_path = [dataset_path + '/' + img_names[i] for i in range(len(img_names))]
search_vectors_via_query(query_path=images_path[query],
                         images_path=images_path,
                         query_vector=img_vectors[query],
                         img_vectors=img_vectors,
                         threshold=threshold,
                         similarity_func='cosine',
                         )