#!/usr/bin/env python3

import os
import tempfile
import numpy as np
import pandas as pd
import librosa

from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth
)

# =====================================================
# CONFIG
# =====================================================

TOKEN = "Jf3e7twd15Ivq1fIYjjbjjaI5m9CSaJW"

INPUT_CSV = "training_manifest.csv"
OUTPUT_CSV = "acoustic_features.csv"

CHECKPOINT_EVERY = 10

# =====================================================
# LOAD TRAINING MANIFEST
# =====================================================

manifest = pd.read_csv(INPUT_CSV)

# =====================================================
# RESUME SUPPORT
# =====================================================

if os.path.exists(OUTPUT_CSV):

    existing = pd.read_csv(OUTPUT_CSV)

    rows = existing.to_dict("records")

    done = set(
        existing["file_id"]
        .astype(str)
    )

    print(
        f"Resuming from {len(done)} completed files"
    )

else:

    rows = []

    done = set()

# =====================================================
# BOX CLIENT
# =====================================================

auth = BoxDeveloperTokenAuth(TOKEN)
client = BoxClient(auth)

# =====================================================
# FEATURE EXTRACTION
# =====================================================

def extract_features(y, sr):

    features = {}

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

    for i in range(20):

        features[f"mfcc_{i+1}"] = np.mean(
            mfcc[i]
        )

    features["spectral_centroid"] = np.mean(
        centroid
    )

    features["spectral_bandwidth"] = np.mean(
        bandwidth
    )

    features["spectral_rolloff"] = np.mean(
        rolloff
    )

    features["zcr"] = np.mean(
        zcr
    )

    features["rms"] = np.mean(
        rms
    )

    return features

# =====================================================
# MAIN LOOP
# =====================================================

for idx, row in manifest.iterrows():

    file_id = str(row["file_id"])

    if file_id in done:
        continue

    print(
        f"{idx+1}/{len(manifest)}",
        row["file_name"]
    )

    try:

        stream = client.downloads.download_file(
            file_id
        )

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as tmp:

            while True:

                chunk = stream.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                tmp.write(chunk)

            tmp_path = tmp.name

        y, sr = librosa.load(
            tmp_path,
            sr=8000,
            mono=True
        )

        os.remove(tmp_path)

        feats = extract_features(
            y,
            sr
        )

        feats["file_id"] = file_id
        feats["label"] = row["label"]
        feats["tank"] = row["tank"]

        rows.append(feats)

        done.add(file_id)

        if len(rows) % CHECKPOINT_EVERY == 0:

            pd.DataFrame(rows).to_csv(
                OUTPUT_CSV,
                index=False
            )

            print(
                f"Checkpoint saved ({len(rows)} rows)"
            )

    except Exception as e:

        msg = str(e)

        if "expired" in msg.lower():

            print("\nTOKEN EXPIRED")
            print("Saving checkpoint...")

            pd.DataFrame(rows).to_csv(
                OUTPUT_CSV,
                index=False
            )

            raise SystemExit(0)

        print("FAILED:", e)

# =====================================================
# FINAL SAVE
# =====================================================

pd.DataFrame(rows).to_csv(
    OUTPUT_CSV,
    index=False
)

print()
print("Completed")
print("Rows:", len(rows))
