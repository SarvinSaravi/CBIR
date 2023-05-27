import numpy as np


def generate_permutation(vector):
    # sorted_indexes = np.array(np.argsort(-vector) + 1)
    sorted_indexes = np.argsort(-vector)
    print(sorted_indexes)

    new_list = [(v, i) for i, v in enumerate(sorted_indexes)]
    print(new_list)
    # new_list = new_list.sort()
    # print(new_list)

    lst = [0] * len(new_list)

    for i, v in new_list:
        lst[i] = v

    print(lst)
    # new_array = np.array(new_list)

    # print(np.linalg.inv(sorted_indexes))
    # print(inverse)


vec = np.array([0.1, 0, 0, 0, 0.2, 0, 0.3, 0.4, 0, 0])
generate_permutation(vec)

# [7 6 4 0 1 2 3 5 8 9]
# output should be this: [3, 4, 5, 6, 2, 7, 1, 0, 8, 9]
