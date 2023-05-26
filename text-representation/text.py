# import numpy as np


def generate_text(vector, k):
    text_vector = []
    for i in range(1, k + 1):
        v = vector[i - 1]
        Ti = "T" + str(i)
        rep = (k + 1) - v
        text_vector.append(Ti * rep)

    text_vector.sort(key=len, reverse=True)
    text = ''.join(text_vector)
    print(text)
    return text


# GPT optimization - the main method should be used
def generate_text_opt(vector, k):
    Ti = [f"T{i}" for i in range(1, len(vector) + 1)]
    vector = [x if x <= k else (k + 1) for x in vector]
    text_vector = [Ti[i] * (k + 1 - v) for i, v in enumerate(vector)]
    text_vector.sort(key=len, reverse=True)
    text = ''.join(text_vector)
    print(text)


def generate_txt_truncate(tr_vector, k):
    text_vector = []
    tr_vector = [x if x <= k else (k + 1) for x in tr_vector]
    for i in range(1, len(tr_vector) + 1):
        v = tr_vector[i - 1]
        Ti = "T" + str(i)
        rep = (k + 1) - v
        text_vector.append(Ti * rep)

    text_vector.sort(key=len, reverse=True)
    text = ''.join(text_vector)
    print(text)
    return text


# examples for test
# vector = [3, 2, 4, 5, 1]
# k = len(vector)
# generate_text_opt(vector, k)
# output should be this: T5T5T5T5T5T2T2T2T2T1T1T1T3T3T4

# vector = [4, 5, 6, 7, 3, 8, 2, 1, 9, 10]
# k = 4
# generate_text_opt(vector, k)
# output should be this: T8T8T8T8T7T7T7T5T5T1
