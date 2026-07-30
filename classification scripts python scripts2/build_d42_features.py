import pandas as pd
import numpy as np

df = pd.read_csv(
    "d42_dataset.csv"
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

df["spl_proxy"] = (
    20
    *
    np.log10(
        np.maximum(
            df["rms"],
            1e-9
        )
    )
)

df["burst_proxy"] = (
    np.abs(
        df["mfcc_1"]
    )
    *
    df["zcr"]
)

df["turbulence_proxy"] = (
    df["rms"]
    *
    df["spectral_bandwidth"]
)

df["spectral_energy_proxy"] = (
    df["spectral_centroid"]
    *
    df["spectral_bandwidth"]
)

df.to_csv(
    "d42_features.csv",
    index=False
)

print(df.shape)
