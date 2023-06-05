import numpy as np


def generate_permutation(vector):
    sorted_indexes = np.argsort(-vector)
    # print(sorted_indexes)  # array of indexes in descending order

    lst = np.zeros_like(sorted_indexes)

    for i, v in enumerate(sorted_indexes):
        lst[v] = i + 1

    # print(lst)
    return np.array(lst)


# some examples to test
# vec = np.array([0.1, 0, 0, 0, 0.2, 0, 0.3, 0.4, 0, 0])
# generate_permutation(vec)
# output should be this: [7 6 4 0 1 2 3 5 8 9]  ====>    [4, 5, 6, 7, 3, 8, 2, 1, 9, 10]

# vec = np.array([[1.23634, 6.23, 3.3333, 10.2, 0, 0, 5.800453, 1.236, 0, 0],
#                [0.1, 0, 0, 0, 0.2, 0, 0.3, 0.4, 0, 0],
#                [0.1, 0, 0.111, 0, 0.2, 0.2, 0.3, 0.4, 0.1, 2]])
#
# result = np.apply_along_axis(generate_permutation, axis=1, arr=vec)
# print(vec.shape) # (3,10)
# print(result)
# output should be this :
# [[ 5  2  4  1  7  8  3  6  9 10]
#  [ 4  5  6  7  3  8  2  1  9 10]
#  [ 7  9  6 10  4  5  3  2  8  1]]
