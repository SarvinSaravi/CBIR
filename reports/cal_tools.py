from reports import image_viewer as show
from similarity import load_similarity


def compare_with_threshold(scores,
                           threshold,
                           ) -> list:
    similar_images = list()
    for i, result in enumerate(scores):
        if result > threshold:
            print(result)
            similar_images.append(i)

    return similar_images


def similarity_check(query_vector,
                   vectors,
                   similarity_func: str,
                   ) -> list:
    measurement = load_similarity(similarity_name=similarity_func)
    return measurement(query_vector,
                       vectors)


def show_search_results(query_path: str,
                        images_path: list,
                        similar_images,
                        ):
    show.show_image_from_path(query_path, "query")
    for idx in similar_images:
        show.show_image_from_path(images_path[idx], "Similar Images")
    return
