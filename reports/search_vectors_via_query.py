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
