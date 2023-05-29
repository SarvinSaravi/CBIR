from reports import image_viewer as show
from similarity import load_similarity


def compare_with_threshold(scores,
                           threshold,
                           ):
    similar_images = list()
    for i, result in enumerate(scores):
        if result > threshold:
            print(result)
            similar_images.append(i)

    return similar_images


def cal_similarity(query_vector,
                   img_vectors,
                   similarity_func: str,
                   ):
    measurement = load_similarity(similarity_name=similarity_func)
    scores = list()
    for i in range(len(img_vectors)):
        scores.append(measurement(query_vector.reshape(1, -1),
                                  img_vectors[i].reshape(1, -1),
                                  )
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


def search_via_query(query_path: str,
                     images_path: list,
                     query_vector,
                     img_vectors,
                     threshold,
                     similarity_func='cosine',
                     ):
    scores = cal_similarity(query_vector=query_vector,
                            img_vectors=img_vectors,
                            similarity_func=similarity_func,
                            )
    similar_images = compare_with_threshold(scores, threshold)
    show_search_results(query_path,
                        images_path,
                        similar_images,
                        )
    print(" > Finding similar Images is Done!")
    return
