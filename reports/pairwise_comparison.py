import numpy as np
from reports.cal_tools import cal_similarity


def compare_pairwise(img_vectors):
    all_scores = list()
    for vector in img_vectors:
        scores = cal_similarity(vector, img_vectors, 'cosine')
        all_scores.append(scores)
    all_scores = np.array(all_scores)
    # all_scores.reshape(50,50)
    return all_scores

