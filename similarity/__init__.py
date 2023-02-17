from .cosine_similarity import cosine

similarity_type = dict(cosine=cosine,
                       )



def load_model(similarity_name, **kwargs):
    """Get similartiy mesurment"""
    return similarity_type[similarity_name](**kwargs)

