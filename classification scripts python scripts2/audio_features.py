import tempfile
import os
import io
import numpy as np
import pandas as pd
import librosa

from boxsdk import Client
from boxsdk import OAuth2

ACCESS_TOKEN = "7OlKbASEdbXXu8ZGMLBAqneL3im1DBsw"

oauth = OAuth2(
    client_id=None,
    client_secret=None,
    access_token=ACCESS_TOKEN
)

client = Client(oauth)

inventory = pd.read_csv("audio_labelled_dataset.csv")

features = []

for _, row in inventory.iterrows():

    file_id = row["file_id"]  # MUST HAVE BOX FILE ID

    try:

        box_file = client.file(file_id)

        content = box_file.content()

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as tmp:

            tmp.write(content)

            temp_path = tmp.name

        y, sr = librosa.load(
            temp_path,
            sr=None,
            mono=True
        )

        os.unlink(temp_path)

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

        d = {
            "file_id": file_id,
            "label": row["binary_label"],
            "tank_id": row["tank_id"],
            "duration": len(y)/sr,
            "zcr": np.mean(zcr),
            "rms": np.mean(rms),
            "centroid": np.mean(centroid),
            "bandwidth": np.mean(bandwidth),
            "rolloff": np.mean(rolloff)
        }

        for i in range(20):
            d[f"mfcc_{i+1}"] = float(
                np.mean(mfcc[i])
            )

        features.append(d)

        if len(features) % 100 == 0:
            print("Processed:", len(features))

    except Exception as e:

        print(
            "FAILED",
            file_id,
            str(e)
        )

pd.DataFrame(features).to_csv(
    "audio_features.csv",
    index=False
)
