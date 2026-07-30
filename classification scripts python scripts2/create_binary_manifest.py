import pandas as pd

df = pd.read_csv("protocol_manifest.csv")

feeding = df[df["protocol_label"] == "feeding"]

background = (
    df[df["protocol_label"] == "baseline"]
    .sample(len(feeding), random_state=42)
)

binary = pd.concat(
    [feeding, background]
)

binary.to_csv(
    "binary_manifest.csv",
    index=False
)

print(binary["protocol_label"].value_counts())

