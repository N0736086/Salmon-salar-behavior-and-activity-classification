import pandas as pd

features = pd.read_csv(
    "segment_features.csv"
)

manifest = pd.read_csv(
    "protocol_segment_manifest.csv"
)

out = features.merge(

    manifest[
        [
            "segment_file",
            "protocol_label"
        ]
    ],

    on="segment_file",

    how="inner"
)

out.to_csv(
    "protocol_segment_features.csv",
    index=False
)

print(out.shape)

print(
    out["protocol_label"]
    .value_counts()
)
