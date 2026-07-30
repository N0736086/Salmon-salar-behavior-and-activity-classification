import pandas as pd

df = pd.read_csv(
    "protocol_recordings.csv"
)

df = df.rename(
    columns={
        "name":"filename"
    }
)

df.to_csv(
    "protocol_manifest_v2.csv",
    index=False
)

print(df.shape)

print(
    df["protocol_label"]
    .value_counts()
)
