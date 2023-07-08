import pandas as pd
import subprocess
import os


def get_queries():
    """
        this function read baseline_result_200806.dat and make a list of queries(image titles)
        instead of baseline_result_200806.dat can use:
           evaluation/he_wgc_result_200806.dat
           evaluation/perfect_result.dat
    """
    file_path = os.path.join(os.path.dirname(__file__), 'baseline_result_200806.dat')
    df = pd.read_csv(file_path, delimiter='\t', header=None)
    query_list = []
    for i in range(df.size):
        query_list.append(df.iloc[i][0][0:10])

    return query_list


def result_assessment(results: dict, file_name):
    """
            result is a python dictionary (similar to JSON) that:
                    keys = query (image title)
                    values = elasticsearch response for this query + a dictionary form like:
                        keys = similar images (image title)
                        values = score of this similar image (How similar is it)
    """
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'w') as file:
        for query, response in results.items():
            result_line = query + ' '
            rank = 0
            # sort response object based on value of scores
            sorted_response = dict(sorted(response.items(), key=lambda x: x[1], reverse=True))
            for result_image_name in sorted_response.keys():
                result_line += (str(rank) + ' ' + result_image_name + ' ')
                rank += 1
            file.write(result_line + '\n')

    # holiday_script = os.path.join(os.path.dirname(__file__), 'holidays_map.py')
    # command = 'python ' + holiday_script + ' ' + file_path
    # subprocess.call(command, shell=True)

# test-case for understand result structure and make result file
# res = {
#     '125800.jpg': {
#         '125800.jpg': 20.6656,
#         '125801.jpg': 2.4323,
#         '125802.jpg': 2.63278
#     },
#     '144400.jpg': {
#         '144401.jpg': 5.23232,
#         '144400.jpg': 12.96878
#     }
# }
# result_assessment(res, 'map.dat')
