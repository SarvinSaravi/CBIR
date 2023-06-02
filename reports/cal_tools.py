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


def cal_similarity(query_vector,
                   img_vectors,
                   similarity_func: str,
                   ) -> list:
    measurement = load_similarity(similarity_name=similarity_func)
    scores = list()
    for i in range(len(img_vectors)):
        scores.append(measurement(query_vector.reshape(1, -1),
                                  img_vectors[i].reshape(1, -1),
                                  )[0][0]
                      )
    return scores


def show_search_results(query_path: str,
                        images_path: list,
                        similar_images,
                        ):
    show.show_image_from_path(query_path, "query")
    for idx in similar_images:
        show.show_image_from_path(images_path[idx], "Similar Images")
    return
