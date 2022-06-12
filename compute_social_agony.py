import argparse
import os.path
from time import time

from file_io import read_dict_from_file
from helper_funs import dir_tail_name, run_command

AGONY_PATH = "agony/agony"


def compute_social_agony(graph_file):
    dir_name, tail = dir_tail_name(graph_file)
    output = os.path.join(dir_name, tail.split(".")[0] + "_socialagony.txt")
    command = f"{AGONY_PATH} {graph_file} {output}"
    print(f"running command: {command}")
    start = time()
    run_command(command)
    end = time()
    time_used = end - start
    print(f"time used in computing social agony: {time_used:0.4f} s")
    print("====compute agony done=====")
    agony_score = read_dict_from_file(output)
    return agony_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph_file", default=" ", help="input graph file name (edges list)")
    args = parser.parse_args()
    graph_file = args.graph_file
    compute_social_agony(graph_file)
