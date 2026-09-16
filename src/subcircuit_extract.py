import pandas as pd
from pathlib import Path

path = Path("/Users/daniel/Desktop/Fly")

NEURONS = ["LPLC2", "LC4", "LC10", "DNp01", "DNp11", "DNa01", "DNa02", "DNb01", "DNp09", "MDN", "DNp10", "OCG", "AOTU019", "AOTU025", "DNa03", "pC1", "DNg02", "DNg07", "DNg13", "DNa11", "DNae014", "LAL013"]
NAUGHTY_LIST = ["LPLC4", "LC40", "LC41", "LC43", "LC44", "LC45", "LC46", "DNp104", "DNp102", "DNp101", "mALC4", "DNp103"]

def neuron_finder():
    df = annotations
    df_filtered = df[(df["flywireType"].str.contains("|".join(NEURONS),case=True, na=False)) & (~df["flywireType"].isin(NAUGHTY_LIST))]
    df_filtered.reset_index(drop=True).to_feather(path / "neuron_annotations.feather")

def subcircuit_extract():
    df = weights
    neurons = pd.read_feather(path / "neuron_annotations.feather")
    body_id = set(neurons["bodyId"])
    connections = df[(df["body_pre"].isin(body_id)) & (df["body_post"].isin(body_id))]
    connections.reset_index(drop=True).to_feather(path / "truncated_connections.feather")

if __name__ == "__main__":
    annotations = pd.read_feather(path / "body-annotations-male-cns-v1.0-minconf-0.5.feather")
    weights = pd.read_feather(path / "connectome-weights-male-cns-v1.0-minconf-0.5.feather")
    neuron_finder()
    subcircuit_extract()
