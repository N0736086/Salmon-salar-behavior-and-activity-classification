import pandas as pd

df = pd.read_csv("segment_features.csv")

def protocol_label(x):

    if x == "feeding":
        return "feeding"

    return "baseline"

df["protocol_label"] = (
    df["label"]
    .apply(protocol_label)
)

df.to_csv(
    "protocol_features.csv",
    index=False
)

print(
    df["protocol_label"]
    .value_counts()
)

