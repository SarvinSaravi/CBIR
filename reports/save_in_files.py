import numpy as np
import os
import csv


def save_in_npz(data,
                hyperparams=None,
                file_dir="results/npz",
                file_name="default",
                ):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path = f"{file_dir}/{file_name}"
    if not file_path.endswith(".npz"):
        file_path = file_path + ".npz"

    np.savez(file_path, **data)
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
    file_path = file_dir + "/" + file_name
    if not file_path.endswith(".csv"):
        file_path = file_path + ".csv"
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(zip(*data))
    print("Saving to", file_path, "is done!")
    return
