from .cosine_similarity import cosine
from .bm25_similarity import bm25

similarity_type = dict(cosine=cosine,
                       bm25=bm25,
                       )


def load_similarity(similarity_name, **kwargs):
    """Get similarity measurement"""
    return similarity_type[similarity_name](**kwargs)
