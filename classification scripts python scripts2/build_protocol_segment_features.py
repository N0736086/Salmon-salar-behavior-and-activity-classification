import pandas as pd

features = pd.read_csv(
    "segment_features.csv"
)

labels = pd.read_csv(
    "segment_manifest_protocol.csv"
)

out = features.merge(

    labels[
        [
            "segment_file",
            "protocol_label"
        ]
    ],

    on="segment_file",
    how="inner"
)

out.to_csv(
    "segment_features_protocol.csv",
    index=False
)

print(out.shape)

print(
    out["protocol_label"]
    .value_counts()
)
