import numpy as np


def generate_permutation(vector):
    sorted_indexes = np.argsort(-vector)
    # print(sorted_indexes)

    lst = [0] * len(vector)

    for i, v in enumerate(sorted_indexes):
        lst[v] = i + 1

    # print(lst)
    return lst


# some examples to test
# vec = np.array([1.23634, 6.23, 3.3333, 10.2, 5.800453, 1.236])
# generate_permutation(vec)
#  output should be this: [3, 1, 4, 2, 0, 5]    ===>     [5, 2, 4, 1, 3, 6]

# vec = np.array([0.1, 0, 0, 0, 0.2, 0, 0.3, 0.4, 0, 0])
# generate_permutation(vec)
# output should be this: [7 6 4 0 1 2 3 5 8 9]  ====>    [4, 5, 6, 7, 3, 8, 2, 1, 9, 10]
