# import numpy as np


def generate_text(vector, k, **kwargs):
    text_vector = []
    for i in range(1, k + 1):
        v = vector[i - 1]
        Ti = "T" + str(i)
        rep = (k + 1) - v
        text_vector.append(Ti * rep)

    text_vector.sort(key=len, reverse=True)
    text = ''.join(text_vector)
    print(text)


exp_vector = [4, 2, 3, 5, 1]
exp_k = len(exp_vector)

generate_text(exp_vector, exp_k)
