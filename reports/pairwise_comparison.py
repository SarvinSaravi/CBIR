import numpy as np
from reports.cal_tools import cal_similarity


def compare_pairwise(vectors,
                     similarity_func='cosine',
                     ):
    all_scores = list()
    for vector in vectors:
        scores = cal_similarity(vector, vectors, similarity_func)
        all_scores.append(scores)
    all_scores = np.array(all_scores)
    return all_scores

