import pandas as pd

df = pd.read_csv("behaviour_events.csv")

# parse dd-mm-yyyy dates
df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%m-%Y",
    errors="coerce"
)

print("Invalid dates:", df["date"].isna().sum())

# remove bad rows
df = df[df["date"].notna()].copy()

df["start_datetime"] = pd.to_datetime(
    df["date"].dt.strftime("%Y-%m-%d")
    + " "
    + df["start_time"].astype(str),
    errors="coerce"
)

df["end_datetime"] = pd.to_datetime(
    df["date"].dt.strftime("%Y-%m-%d")
    + " "
    + df["end_time"].astype(str),
    errors="coerce"
)

df.to_csv(
    "behaviour_windows.csv",
    index=False
)

print(df.shape)

print(
    df[
        [
            "tank_id",
            "behaviour_code",
            "start_datetime",
            "end_datetime"
        ]
    ].head()
)
