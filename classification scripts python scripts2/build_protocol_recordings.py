import pandas as pd

events = pd.read_csv(
    "protocol_events_2026.csv"
)

events["start_datetime"] = pd.to_datetime(
    events["start_datetime"]
)

events["end_datetime"] = pd.to_datetime(
    events["end_datetime"]
)

recs = pd.read_csv(
    "recording_times_clean.csv"
)

recs["recording_start"] = pd.to_datetime(
    recs["recording_start"]
)

matches = []

for _, rec in recs.iterrows():

    t = rec["recording_start"]

    overlap = events[
        (events["start_datetime"] <= t)
        &
        (events["end_datetime"] >= t)
    ]

    if overlap.empty:
        continue

    # priority:
    # feeding > stress > baseline

    labels = set(
        overlap["protocol_label"]
    )

    if "feeding" in labels:
        label = "feeding"
    elif "stress" in labels:
        label = "stress"
    else:
        label = "baseline"

    matches.append({
        "name": rec["name"],
        "path": rec["path"],
        "recording_start": t,
        "protocol_label": label
    })

out = pd.DataFrame(matches)

out.to_csv(
    "protocol_recordings.csv",
    index=False
)

print(out.shape)

print(
    out["protocol_label"]
    .value_counts()
)
