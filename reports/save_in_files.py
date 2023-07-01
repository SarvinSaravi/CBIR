import numpy as np
import os
import csv


def save_in_npz(data,
                hyperparams: dict,
                file_dir="results/npz",
                file_name="default",
                ):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if file_name == "S":
        file_name = f"data_k{hyperparams['K']}_S{hyperparams['S']}"
    elif file_name == "L":
        file_name = f"data_k{hyperparams['K']}_l{hyperparams['L']}"
    file_path = file_dir + "/" + file_name + ".npz"
    np.savez(file_path, data=data, hyperparams=hyperparams)
    print("Saving to", file_path, "is done!")
    return


def save_in_csv(data,
                hyperparams = None,
                file_dir="results/csv",
                file_name="S",
                ):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if file_name == "S":
        file_name = f"data_K{hyperparams['K']}_S{hyperparams['S']}"
    elif file_name == "L":
        file_name = f"data_K{hyperparams['K']}_l{hyperparams['L']}"
    file_path = file_dir + "/" + file_name + ".csv"
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(zip(*data))
    print("Saving to", file_path, "is done!")
    return
