# import numpy as np


# Use this function when k=len(vector)
def generate_text(vector, k):
    text_vector = []
    for i in range(1, k + 1):
        v = vector[i - 1]
        Ti = "T" + str(i)
        rep = (k + 1) - v
        text_vector.append(Ti * rep)

    text_vector.sort(key=len, reverse=True)
    text = ''.join(text_vector)
    # print(text)
    return text


# Use this function along with the desired k for truncate string
def generate_txt_truncate(tr_vector, k):
    text_vector = []
    tr_vector = [x if x <= k else (k + 1) for x in tr_vector]  # apply k
    for i in range(1, len(tr_vector) + 1):
        v = tr_vector[i - 1]
        Ti = "T" + str(i)
        rep = (k + 1) - v
        text_vector.append(Ti * rep)

    text_vector.sort(key=len, reverse=True)
    text = ''.join(text_vector)
    # print(text)
    return text


# The main method should be used (Optimize version of previous function)
def generate_text_opt(vector, k):
    Ti = [f"T{i}" for i in range(1, len(vector) + 1)]
    vector = [x if x <= k else (k + 1) for x in vector]  # apply k
    text_vector = [Ti[i] * (k + 1 - v) for i, v in enumerate(vector)]
    text_vector.sort(key=sortByT, reverse=True)
    text = ' '.join(text_vector)
    # print(text)
    return text.rstrip()


def sortByT(val):
    return val.count('T')


def generate_text_with_separator(vector, k):
    Ti = [f"T{i} " for i in range(1, len(vector) + 1)]  # different here than previous
    vector = [x if x <= k else (k + 1) for x in vector]  # apply k
    text_vector = [Ti[i] * (k + 1 - v) for i, v in enumerate(vector)]
    text_vector.sort(key=sortByT, reverse=True)
    text = ''.join(text_vector)
    # print(text)
    return text.rstrip()

# examples for test
# vector = [3, 2, 4, 5, 1]
# k = len(vector)
# generate_text_opt(vector, k)
# output should be this: T5T5T5T5T5T2T2T2T2T1T1T1T3T3T4

# vector = [7, 9, 6, 10, 4, 5, 3, 2, 8, 1]
# k = 4
# print(generate_text_opt(vector, k))
# output should be this: T10T10T10T10T8T8T8T7T7T5

# vector = np.array([[5, 2, 4, 1, 7, 8, 3, 6, 9, 10],
#                    [4, 5, 6, 7, 3, 8, 2, 1, 9, 10],
#                    [7, 9, 6, 10, 4, 5, 3, 2, 8, 1]])
# k = 3
# result = np.apply_along_axis(generate_text_opt, axis=1, arr=vector, k=k)
# print(result)
# result = list(generate_text_with_separator(item, k) for item in vector)
# print(result)
# for i, v in enumerate(result):
#     print(i, v)
