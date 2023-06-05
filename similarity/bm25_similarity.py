from rank_bm25 import BM25Okapi as BM25


def split_g_gram(string, g):
    result = list()
    n = len(string)
    if n >= g:
        for i in range(n + 1 - g):
            result.append(string[i:i+g])
    return result


def cal_bm25(query, corpus, g=4):
    corpus_tokens = list()
    for doc in corpus:
        corpus_tokens.append(split_g_gram(doc, g))
    bm25 = BM25(corpus_tokens)
    query_tokens = split_g_gram(query, g)
    scores = bm25.get_scores(query_tokens)
    normalized_scores = [(x - min(scores)) / (max(scores) - min(scores)) for x in scores]
    # print(len(normalized_scores))
    return normalized_scores


def bm25():
    return cal_bm25
