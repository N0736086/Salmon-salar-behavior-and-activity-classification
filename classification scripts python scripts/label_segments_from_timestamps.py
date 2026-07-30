import pandas as pd

segments = pd.read_csv(
    "segment_manifest.csv"
)

audio = pd.read_csv(
    "training_manifest_fixed.csv"
)

windows = pd.read_csv(
    "event_windows.csv"
)

audio["timestamp"] = pd.to_datetime(
    audio["timestamp"]
)

windows["start"] = pd.to_datetime(
    windows["start"]
)

windows["end"] = pd.to_datetime(
    windows["end"]
)

audio["file_id"] = (
    audio["file_id"]
    .astype(str)
)

segments["file_id"] = (
    segments["file_id"]
    .astype(str)
)

segments = segments.merge(
    audio[
        ["file_id","timestamp"]
    ],
    on="file_id",
    how="left"
)

def assign_label(ts):

    m = windows[
        (windows["start"] <= ts)
        &
        (windows["end"] >= ts)
    ]

    if len(m) == 0:
        return "baseline"

    return (
        m.iloc[0]
        ["protocol_label"]
    )

segments["protocol_label"] = (
    segments["timestamp"]
    .apply(assign_label)
)

segments.to_csv(
    "segment_manifest_protocol.csv",
    index=False
)

print(
    segments["protocol_label"]
    .value_counts()
)
