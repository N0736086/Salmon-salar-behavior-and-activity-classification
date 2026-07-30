import pandas as pd

df = pd.read_csv("behaviour_windows.csv")

df = df[
    df["behaviour_code"].isin(
        ["P1","P2","P3","P4","P5","P6"]
    )
].copy()

df = df[
    df["tank_id"].notna()
]

cols = [
    "tank_id",
    "behaviour_code",
    "behaviour_label",
    "start_datetime",
    "end_datetime",
    "comments"
]

df = df[cols]

df.to_csv(
    "labelled_behaviour_events.csv",
    index=False
)

print(df.shape)

print(
    df["tank_id"]
    .value_counts()
)

print(
    df["behaviour_code"]
    .value_counts()
)
