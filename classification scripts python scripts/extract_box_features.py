# extract_box_features.py

import tempfile
import os
import requests
import librosa
import numpy as np
import pandas as pd

TOKEN = "T5i0pNyGt3VUnMnsXdn7CCpYxpAvNMdz"

INPUT_FILE = "audio_box_files.csv"
OUTPUT_FILE = "audio_features.csv"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

df = pd.read_csv(INPUT_FILE)

results = []

for i, row in df.iterrows():

    file_id = str(row["file_id"])

    try:

        url = (
            f"https://api.box.com/2.0/files/"
            f"{file_id}/content"
        )

        r = requests.get(
            url,
            headers=HEADERS,
            stream=True,
            allow_redirects=True,
            timeout=300
        )

        if r.status_code != 200:
            print("FAILED DOWNLOAD", file_id)
            continue

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as tmp:

            for chunk in r.iter_content(
                chunk_size=1024 * 1024
            ):
                tmp.write(chunk)

            temp_wav = tmp.name

        y, sr = librosa.load(
            temp_wav,
            sr=None,
            mono=True
        )

        os.remove(temp_wav)

        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=20
        )

        rms = librosa.feature.rms(y=y)

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

        feat = {
            "file_id": file_id,
            "tank_id": row["tank_id"],
            "label": row["binary_label"],

            "duration": len(y) / sr,

            "rms_mean": float(np.mean(rms)),
            "zcr_mean": float(np.mean(zcr)),
            "centroid_mean": float(np.mean(centroid)),
            "bandwidth_mean": float(np.mean(bandwidth)),
            "rolloff_mean": float(np.mean(rolloff))
        }

        for m in range(20):
            feat[f"mfcc_{m+1}"] = float(
                np.mean(mfcc[m])
            )

        results.append(feat)

        if len(results) % 50 == 0:

            pd.DataFrame(results).to_csv(
                OUTPUT_FILE,
                index=False
            )

            print(
                f"Processed {len(results)}"
            )

    except Exception as e:

        print(
            "FAILED",
            file_id,
            e
        )

pd.DataFrame(results).to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "DONE:",
    len(results)
)
