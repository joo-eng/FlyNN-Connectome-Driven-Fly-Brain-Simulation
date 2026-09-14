import pandas as pd
df = pd.read_feather("/Users/daniel/Desktop/Fly/body-annotations-male-cns-v1.0-minconf-0.5.feather")
neurons = ["LPLC2", "LC4", "LC10", "DNp01", "DNp11", "DNa01", "DNa02", "DNb01", "DNp09", "MDN", "DNp10", "OCG", "AOTU019", "AOTU025", "DNa03", "pC1"]
naughty_list = ["LPLC4", "LC40", "LC41", "LC43", "LC44", "LC45", "LC46", "DNp104", "DNp102", "DNp101", "mALC4", "DNp103"]
df_filtered = df[(df["flywireType"].str.contains("|".join(neurons),case=True, na=False)) & (~df["flywireType"].isin(naughty_list))]
df_filtered.reset_index(drop=True).to_feather("/Users/daniel/Desktop/Fly/neuron_annotations.feather")
print(df_filtered)
