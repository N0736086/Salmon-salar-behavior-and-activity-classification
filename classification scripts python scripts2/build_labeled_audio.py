#!/usr/bin/env python3

import pandas as pd

audio = pd.read_csv(
    "master_annotations.csv"
)

eth = pd.read_csv(
    "ethogram_clean.csv"
)

audio["timestamp"] = pd.to_datetime(
    audio["timestamp"],
    errors="coerce"
)

eth["Date"] = pd.to_datetime(
    eth["Date"],
    dayfirst=True,
    errors="coerce"
)

eth["start"] = pd.to_datetime(
    eth["Date"].dt.strftime("%Y-%m-%d")
    + " "
    + eth["Time entered"].astype(str),
    errors="coerce"
)

eth["end"] = pd.to_datetime(
    eth["Date"].dt.strftime("%Y-%m-%d")
    + " "
    + eth["Exit time"].astype(str),
    errors="coerce"
)

eth = eth[
    eth["label"].notna()
]

results = []

for _, a in audio.iterrows():

    ts = a["timestamp"]

    if pd.isna(ts):
        continue

    matches = eth[
        (eth["start"] <= ts)
        &
        (eth["end"] >= ts)
    ]

    if len(matches) == 0:

        results.append({
            "file_id": a["file_id"],
            "file_name": a["file_name"],
            "tank": a["tank"],
            "tank_type": a["tank_type"],
            "timestamp": ts,
            "label": "background"
        })

    else:

        m = matches.iloc[0]

        results.append({
            "file_id": a["file_id"],
            "file_name": a["file_name"],
            "tank": a["tank"],
            "tank_type": a["tank_type"],
            "timestamp": ts,
            "label": m["label"]
        })

labeled = pd.DataFrame(results)

labeled.to_csv(
    "labeled_audio.csv",
    index=False
)

print()

print("Saved labeled_audio.csv")

print()

print(
    labeled["label"]
    .value_counts()
)
