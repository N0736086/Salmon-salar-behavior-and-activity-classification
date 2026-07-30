import pandas as pd

df = pd.read_csv(
    "recording_times.csv"
)

df["recording_start"] = pd.to_datetime(
    df["recording_start"]
)

df = df[
    df["recording_start"] >= "2026-01-01"
]

df.to_csv(
    "recording_times_clean.csv",
    index=False
)

print(df.shape)

print(
    df["recording_start"].min()
)

print(
    df["recording_start"].max()
)
