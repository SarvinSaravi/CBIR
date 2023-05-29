from similarity import load_similarity
from reports.cal_tools import *


def search_texts_via_query(query_path,
                           images_path,
                           query_string,
                           text_strings,
                           threshold,
                           similarity_func,
                           ):
    measurement = load_similarity(similarity_name=similarity_func)
    scores = measurement(query_string, text_strings)
    similar_images = compare_with_threshold(scores, threshold)
    show_search_results(query_path,
                        images_path,
                        similar_images,
                        )
    print(" > Finding similar Images via their text strings is Done!")
    return
