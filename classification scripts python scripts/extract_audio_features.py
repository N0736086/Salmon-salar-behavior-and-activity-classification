import pandas as pd
import numpy as np
import librosa
from pathlib import Path

dataset = pd.read_csv(
    "audio_labelled_dataset.csv"
)

features = []

for idx, row in dataset.iterrows():

    wav = row["full_path"]

    try:

        y, sr = librosa.load(
            wav,
            sr=None,
            mono=True
        )

        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=20
        )

        zcr = librosa.feature.zero_crossing_rate(y)

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

        rms = librosa.feature.rms(y=y)

        row_features = {

            "file_name": row["file_name"],
            "tank_id": row["tank_id"],
            "label": row["binary_label"],

            "zcr_mean": np.mean(zcr),
            "rms_mean": np.mean(rms),

            "centroid_mean": np.mean(centroid),
            "bandwidth_mean": np.mean(bandwidth),
            "rolloff_mean": np.mean(rolloff)
        }

        for i in range(20):

            row_features[f"mfcc_{i+1}"] = np.mean(
                mfcc[i]
            )

        features.append(row_features)

    except Exception as e:

        print("FAILED:", wav)
        print(e)

        continue

    if len(features) % 100 == 0:

        print("Processed", len(features))

df = pd.DataFrame(features)

df.to_csv(
    "audio_features.csv",
    index=False
)

print(df.shape)

print(
    df["label"]
    .value_counts()
)
