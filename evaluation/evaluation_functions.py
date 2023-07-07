import pandas as pd


def get_queries():
    df = pd.read_csv('baseline_result_200806.dat', delimiter='\t', header=None)
    query_list = []
    for i in range(df.size):
        query_list.append(df.iloc[i][0][0:10])

    return query_list
