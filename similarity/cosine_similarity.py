from sklearn.metrics.pairwise import cosine_similarity


def call_cosine(query,
                vectors,
                ):
    scores = list()
    for i in range(len(vectors)):
        scores.append(cosine_similarity(query.reshape(1, -1),
                                        vectors[i].reshape(1, -1),
                                        )[0][0]
                      )
    return scores


def cosine():
    return call_cosine
