from .cosine_similarity import cosine

similarity_type = dict(cosine=cosine,
                       )


def load_similarity(similarity_name, **kwargs):
    """Get similarity measurement"""
    return similarity_type[similarity_name](**kwargs)
