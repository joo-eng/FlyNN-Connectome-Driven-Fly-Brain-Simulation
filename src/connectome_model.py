import numpy as np
import pandas as pd
from pathlib import Path

path = Path("/Users/daniel/Desktop/Fly")

RATE = 0.5
INPUTS = ["LPLC2", "LC4", "LC10a", "OCG01a", "OCG01b", "OCG01c", "OCG01d", "OCG01e", "OCG01f", "OCG02a", "OCG02b", "OCG02c"]
OUTPUTS = ["DNp01", "DNp11", "DNa02", "DNa01", "DNp09", "MDN", "DNp10", "DNg02_a", "DNg02_b", "DNg02_c", "DNg02_d", "DNg02_e", "DNg02_f", "DNg02_g", "DNg07"]

def matrix_synthesis():
    weight_matrix = np.zeros((N, N))
    body_to_index = {}
    for i, body in enumerate(neurons["bodyId"]):
        body_to_index[body] = i
    row = connections["body_pre"].map(body_to_index).to_numpy()
    column = connections["body_post"].map(body_to_index).to_numpy()
    np.add.at(weight_matrix, (row, column), connections["weight"].to_numpy())
    ask = input("1 for .csv, 2 for .feather, anything else for nothing")
    if ask == "1":
        np.savetxt(path / "weight_matrix.csv", weight_matrix, delimiter=",", fmt="%.6f")
    elif ask == "2":
        df_matrix = pd.DataFrame(weight_matrix)
        df_matrix.columns = df_matrix.columns.astype(str)
        df_matrix.to_feather(path / "weight_matrix.feather")
    return weight_matrix

def vector_update(state_vector, weight_matrix, ext):
    input = (state_vector @ weight_matrix) + ext
    target = np.clip(input, 0, 1)
    new_state = state_vector + RATE * (target - state_vector)
    return new_state

def index_map():
    titles = neurons["flywireType"].to_numpy()
    input_map = {}
    for a, b in enumerate(titles):
        if b in INPUTS:
            if b not in input_map:
                input_map[b] = []
            input_map[b].append(a)
        pass
    output_map = {}
    for c, d in enumerate(titles):
        if d in OUTPUTS:
            if d not in output_map:
                output_map[d] = []
            output_map[d].append(c)
    return input_map, output_map

if __name__ == "__main__":
    connections = pd.read_feather(path / "truncated_connections.feather")
    neurons = pd.read_feather(path / "neuron_annotations.feather")
    N = len(neurons)
    state_vector = np.zeros(N)
    ext = np.zeros(N) # For manual testing/tuning
    weight_matrix = matrix_synthesis()
    input_map, output_map = index_map()
    for tick in range(20):
        state_vector = vector_update(state_vector, weight_matrix, ext)

"""
Inputs (into ext)
LPLC2: how big a looming object is, in each of 24 view directions
LC4: how fast it's expanding, in each of 24 directions
LC10a: how much a small moving target is present, in each of 24 directions (multiplied by arousal)
OCG: roll and pitch vs. the horizon (flight only)
Airborne: whether the fly is flying (0 or 1)

Outputs (read from the state)
DNp01: escape jump when over ~0.8, then a ~200 ms cooldown
DNp11: escape direction
DNa02: turning, from left minus right (main steering)
DNa01: turning, secondary
DNp09: stop
MDN: walk backward
DNp10: land (flight only)
DNg02: flight power, and left minus right for flight turning
DNg07: brake or descend (flight only)"""