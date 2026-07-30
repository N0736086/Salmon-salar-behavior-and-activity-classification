#!/usr/bin/env python3

import pandas as pd

features = pd.read_csv(
    "acoustic_features.csv"
)

manifest = pd.read_csv(
    "training_manifest_fixed.csv"
)

manifest["file_id"] = (
    manifest["file_id"]
    .astype(str)
)

features["file_id"] = (
    features["file_id"]
    .astype(str)
)

features = features.drop(
    columns=["tank"],
    errors="ignore"
)

features = features.merge(
    manifest[
        ["file_id", "tank"]
    ],
    on="file_id",
    how="left"
)

features.to_csv(
    "acoustic_features_fixed.csv",
    index=False
)

print(features["tank"].value_counts())
print(features.shape)
