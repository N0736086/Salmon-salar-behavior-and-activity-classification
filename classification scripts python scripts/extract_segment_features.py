#!/usr/bin/env python3

import librosa
import numpy as np
import pandas as pd
from pathlib import Path

manifest = pd.read_csv(
    "segment_manifest.csv"
)

rows = []

for idx, row in manifest.iterrows():

    segment_file = row["segment_file"]

    label = row["label"]

    tank = row["tank"]

    # locate segment
    candidates = list(
        Path("segments").rglob(segment_file)
    )

    if len(candidates) == 0:
        continue

    wav = str(candidates[0])

    try:

        y, sr = librosa.load(
            wav,
            sr=8000,
            mono=True
        )

        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=20
        )

        centroid = librosa.feature.spectral_centroid(
            y=y,
            sr=sr
        )

        bandwidth = librosa.feature.spectral_bandwidth(
            y=y,
            sr=sr
        )

        rolloff = librosa.feature.spectral_rolloff(
            y=y,
            sr=sr
        )

        zcr = librosa.feature.zero_crossing_rate(
            y
        )

        rms = librosa.feature.rms(
            y=y
        )

        r = {
            "segment_file": segment_file,
            "tank": tank,
            "label": label
        }

        for i in range(20):

            r[f"mfcc_{i+1}"] = np.mean(
                mfcc[i]
            )

        r["spectral_centroid"] = np.mean(
            centroid
        )

        r["spectral_bandwidth"] = np.mean(
            bandwidth
        )

        r["spectral_rolloff"] = np.mean(
            rolloff
        )

        r["zcr"] = np.mean(
            zcr
        )

        r["rms"] = np.mean(
            rms
        )

        rows.append(r)

        if len(rows) % 1000 == 0:

            print(
                f"Processed {len(rows)}"
            )

    except Exception as e:

        print(
            "FAILED:",
            segment_file
        )

feature_df = pd.DataFrame(rows)

feature_df.to_csv(
    "segment_features.csv",
    index=False
)

print(
    "\nSaved segment_features.csv"
)

print(feature_df.shape)
