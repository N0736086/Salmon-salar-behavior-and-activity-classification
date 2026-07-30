# extract_box_features_stream.py

import io
import requests
import librosa
import numpy as np
import pandas as pd
import soundfile as sf

TOKEN = "fy6fg0s48IK4p0RQfKiaRV4AZ7GLJLFJ"

INPUT_CSV = "audio_box_files.csv"
OUTPUT_CSV = "audio_features.csv"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

df = pd.read_csv(INPUT_CSV)

results = []

for idx, row in df.iterrows():

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

            print(
                "DOWNLOAD FAIL",
                file_id,
                r.status_code
            )

            continue

        audio_buffer = io.BytesIO(
            r.content
        )

        y, sr = sf.read(
            audio_buffer
        )

        if len(y.shape) > 1:
            y = np.mean(
                y,
                axis=1
            )

        y = y.astype(np.float32)

        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=20
        )

        rms = librosa.feature.rms(
            y=y
        )

        zcr = librosa.feature.zero_crossing_rate(
            y
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

        feat = {

            "file_id": file_id,
            "tank_id": row["tank_id"],
            "label": row["binary_label"],

            "duration_sec": len(y) / sr,

            "rms_mean":
                float(np.mean(rms)),

            "zcr_mean":
                float(np.mean(zcr)),

            "centroid_mean":
                float(np.mean(centroid)),

            "bandwidth_mean":
                float(np.mean(bandwidth)),

            "rolloff_mean":
                float(np.mean(rolloff))
        }

        for i in range(20):

            feat[f"mfcc_{i+1}"] = float(
                np.mean(
                    mfcc[i]
                )
            )

        results.append(
            feat
        )

        if len(results) % 25 == 0:

            pd.DataFrame(
                results
            ).to_csv(
                OUTPUT_CSV,
                index=False
            )

            print(
                "Processed",
                len(results)
            )

    except Exception as e:

        print(
            "FAILED",
            file_id
        )

        print(str(e))

        continue

pd.DataFrame(
    results
).to_csv(
    OUTPUT_CSV,
    index=False
)

print()
print(
    "DONE:",
    len(results)
)

