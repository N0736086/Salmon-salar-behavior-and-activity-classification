import pandas as pd

df = pd.read_csv(
    "fish_events_clean.csv"
)

mapping = {

    "P1": "baseline",

    "P2": "baseline",

    "P3": "stress",

    "P4": "stress",

    "P5": "feeding",

    "P6": "stress"
}

df["protocol_label"] = (
    df["Code"]
    .map(mapping)
)

df = df[
    df["protocol_label"]
    .notna()
]

df.to_csv(
    "fish_protocol_labels.csv",
    index=False
)

print(
    df["protocol_label"]
    .value_counts()
)
