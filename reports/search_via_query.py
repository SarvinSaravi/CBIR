from .dataloading import dataloading as
from reports import image_viewer as show
from .similarity import load_similarity
def searching(query_vector,
              img_vectors,
              threshold=0.65,
              similarity_func='cosine'
              ):

    measurement = load_similarity(similarity_name=similarity_func)
    similar_images = list()
    for i in range(len(img_vectors)):
        result = measurement(query_vector.reshape(1, -1),
                             img_vectors[i].reshape(1, -1),
                             )

        if result > threshold:
            print(result)
            similar_images.append(i)

    return similar_images


def search_via_query(query_path:str,
                     images_path:str,
                     query_vector,
                     img_vectors,
                     ):
    similar_images = searching(query_vector,
                               img_vectors)
    show.show_image_from_path(query_path, "query")
    for idx in similar_images:
        show.show_image_from_path(images_path[idx], "Similar Images")
        print(" > Finding similar Images is Done!")
    return