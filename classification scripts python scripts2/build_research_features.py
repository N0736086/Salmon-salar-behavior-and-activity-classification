import pandas as pd
import numpy as np

df = pd.read_csv("segment_features.csv")

# feeding vs baseline

df["protocol_label"] = df["label"].apply(
    lambda x: "feeding" if x == "feeding" else "baseline"
)

mfcc_cols = [
    c for c in df.columns
    if c.startswith("mfcc_")
]

df["mfcc_mean"] = (
    df[mfcc_cols]
    .mean(axis=1)
)

df["mfcc_std"] = (
    df[mfcc_cols]
    .std(axis=1)
)

df["spectral_ratio"] = (
    df["spectral_centroid"]
    /
    (
        df["spectral_bandwidth"]
        + 1e-9
    )
)

df["turbulence_proxy"] = (
    df["rms"]
    *
    df["zcr"]
)

df["burst_proxy"] = (
    np.abs(df["mfcc_1"])
    *
    df["zcr"]
)

df.to_csv(
    "research_features.csv",
    index=False
)

print(df.shape)

print(
    df["protocol_label"]
    .value_counts()
)
