import pandas as pd

proto = pd.read_csv(
    "protocol_recordings.csv"
)

inventory = pd.read_csv(
    "audio_inventory.csv"
)

segments = pd.read_csv(
    "segment_manifest.csv"
)

# attach id to protocol recordings

proto = proto.merge(
    inventory[
        ["id", "name"]
    ],
    on="name",
    how="left"
)

proto["file_id"] = (
    proto["id"]
    .astype(str)
)

segments["file_id"] = (
    segments["file_id"]
    .astype(str)
)

out = segments.merge(

    proto[
        [
            "file_id",
            "protocol_label"
        ]
    ],

    on="file_id",

    how="inner"
)

out.to_csv(
    "protocol_segment_manifest.csv",
    index=False
)

print(out.shape)

print(
    out["protocol_label"]
    .value_counts()
)
