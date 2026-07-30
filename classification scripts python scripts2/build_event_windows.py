import pandas as pd

df = pd.read_csv("fish_protocol_labels.csv")

# Keep only relevant columns

events = df[
    [
        "Date",
        "Time entered",
        "Exit time",
        "BASSINS",
        "Code",
        "Behavior / Activity",
        "protocol_label"
    ]
].copy()

# Remove rows without timestamps

events = events.dropna(
    subset=[
        "Date",
        "Time entered",
        "Exit time"
    ]
)

# Create datetime columns

events["start_datetime"] = pd.to_datetime(
    events["Date"].astype(str)
    + " "
    + events["Time entered"].astype(str),
    dayfirst=True,
    errors="coerce"
)

events["end_datetime"] = pd.to_datetime(
    events["Date"].astype(str)
    + " "
    + events["Exit time"].astype(str),
    dayfirst=True,
    errors="coerce"
)

# Remove malformed rows

events = events[
    events["start_datetime"].notna()
]

events = events[
    events["end_datetime"].notna()
]

# Duration in seconds

events["duration_seconds"] = (
    events["end_datetime"]
    -
    events["start_datetime"]
).dt.total_seconds()

# Keep only sensible events

events = events[
    events["duration_seconds"] > 0
]

events.to_csv(
    "event_windows.csv",
    index=False
)

print(events.shape)

print(
    events[
        [
            "start_datetime",
            "end_datetime",
            "protocol_label"
        ]
    ].head(20)
)

