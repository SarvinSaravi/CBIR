from .partition import partitioning_by_number_segments
from .partition import partitioning_by_length


def partitioning_process(arr, part_k=4, **kwargs):
    """
        call the function like these:
            1) partitioning_process(arr, length=int, part_k=int)
            2) partitioning_process(arr, num_sec=int, part_k=int)

        and it returns a list(string format of every partition) ===> size=number of pictures
    """
    return_list = []
    for key, value in kwargs.items():
        if key == 'length':
            # print(arr)
            # print('len', str(part_k), value)
            return_list = partitioning_by_length(arr, value, part_k)
        elif key == 'num_sec':
            # print(arr)
            # print('num', str(part_k), value)
            return_list = partitioning_by_number_segments(arr, value, part_k)
        else:
            print(" >>> Please specify the length(length) OR number of segments(num_sec) <<< ")

    return return_list
