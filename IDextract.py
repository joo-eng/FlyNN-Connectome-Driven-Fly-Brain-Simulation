import pandas as pd
df = pd.read_feather("/Users/daniel/Desktop/Fly/connectome-weights-male-cns-v1.0-minconf-0.5.feather")
neurons = pd.read_feather("/Users/daniel/Desktop/Fly/neuron_annotations.feather")
body_id = set(neurons["bodyId"])
connections = df[(df["body_pre"].isin(body_id)) & (df["body_post"].isin(body_id))]
connections.reset_index(drop=True).to_feather("/Users/daniel/Desktop/Fly/truncated_connections.feather")