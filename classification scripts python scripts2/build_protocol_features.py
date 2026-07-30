import pandas as pd

features = pd.read_csv("segment_features.csv")
manifest = pd.read_csv("protocol_segment_manifest.csv")

key = manifest.columns[0]

out = features.merge(
    manifest[
        [key,"protocol_label"]
    ],
    on=key,
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
