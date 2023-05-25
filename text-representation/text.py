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


# GPT optimization but not true output!
def generate_text_opt(vector, k, **kwargs):
    Ti = [f"T{i}" for i in range(1, k + 1)]
    text_vector = [Ti[i - 1] * (k + 1 - v) for i, v in enumerate(vector)]
    text_vector.sort(key=lambda x: vector[Ti.index(x)], reverse=True)
    text = ''.join(text_vector)
    print(text)

# example for test
# vector = [3, 2, 4, 5, 1]
# k = len(vector)
# generate_text(vector, k)
# output should be this: T5T5T5T5T5T2T2T2T2T1T1T1T3T3T4
