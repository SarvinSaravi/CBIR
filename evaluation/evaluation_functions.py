import pandas as pd
import subprocess


def get_queries():
    df = pd.read_csv('baseline_result_200806.dat', delimiter='\t', header=None)
    query_list = []
    for i in range(df.size):
        query_list.append(df.iloc[i][0][0:10])

    return query_list


def result_assessment(results: dict, file_path):
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

    command = 'python holidays_map.py ' + file_path
    subprocess.call(command, shell=True)


res = {
    '125800.jpg': {
        '125800.jpg': 20.6656,
        '125801.jpg': 2.4323,
        '125802.jpg': 2.63278
    },
    '144400.jpg': {
        '144401.jpg': 5.23232,
        '144400.jpg': 12.96878
    }
}

result_assessment(res, 'map.dat')
