import pandas as pd

df = pd.read_csv("event_windows.csv")

df["start_datetime"] = pd.to_datetime(
    df["start_datetime"]
)

df["end_datetime"] = pd.to_datetime(
    df["end_datetime"]
)

# Keep only the hydrophone era

df = df[
    (df["start_datetime"] >= "2026-02-01")
    &
    (df["start_datetime"] <= "2026-06-30")
]

df.to_csv(
    "protocol_events_2026.csv",
    index=False
)

print(df.shape)

print(
    df["protocol_label"]
    .value_counts()
)

print(
    df["start_datetime"].min()
)

print(
    df["start_datetime"].max()
)

