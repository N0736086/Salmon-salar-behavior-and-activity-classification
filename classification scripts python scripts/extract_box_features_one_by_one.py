import os
import tempfile
import requests
import librosa
import numpy as np
import pandas as pd

# =====================================================
# CONFIG
# =====================================================

TOKEN = "EtfPFv2QxxxXXfAXkENeFNmxEIuC4j4A"

INPUT_CSV = "audio_box_files.csv"
OUTPUT_CSV = "audio_features.csv"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# =====================================================
# LOAD INPUT
# =====================================================

df = pd.read_csv(
    INPUT_CSV,
    dtype={"file_id": str}
)

# =====================================================
# RESUME SUPPORT
# =====================================================

processed_ids = set()

if os.path.exists(OUTPUT_CSV):

    existing = pd.read_csv(
        OUTPUT_CSV,
        dtype={"file_id": str}
    )

    processed_ids = set(
        existing["file_id"]
        .astype(str)
        .str.strip()
    )

print(
    f"ALREADY PROCESSED: {len(processed_ids)}"
)

# =====================================================
# FEATURE EXTRACTION
# =====================================================

def extract_features(wav_path):

    y, sr = librosa.load(
        wav_path,
        sr=None,
        mono=True
    )

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

    features = {

        "duration_sec": float(len(y)/sr),

        "rms_mean": float(np.mean(rms)),
        "zcr_mean": float(np.mean(zcr)),
        "centroid_mean": float(np.mean(centroid)),
        "bandwidth_mean": float(np.mean(bandwidth)),
        "rolloff_mean": float(np.mean(rolloff))
    }

    for i in range(20):

        features[f"mfcc_{i+1}"] = float(
            np.mean(mfcc[i])
        )

    return features

# =====================================================
# DOWNLOAD ONE FILE
# =====================================================

def download_box_file(file_id):

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

    if r.status_code == 401:

        print("\nTOKEN EXPIRED")
        return "TOKEN_EXPIRED"

    if r.status_code != 200:

        print(
            f"DOWNLOAD FAIL {file_id} {r.status_code}"
        )

        return None

    tmp = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    for chunk in r.iter_content(
        chunk_size=1024 * 1024
    ):

        if chunk:
            tmp.write(chunk)

    tmp.close()

    return tmp.name

# =====================================================
# PROCESS FILES
# =====================================================

processed_this_run = 0

for _, row in df.iterrows():

    file_id = str(
        row["file_id"]
    ).strip()

    if file_id in processed_ids:
        continue

    wav_file = download_box_file(
        file_id
    )

    if wav_file == "TOKEN_EXPIRED":
        break

    if wav_file is None:
        continue

    try:

        feat = extract_features(
            wav_file
        )

        os.remove(
            wav_file
        )

        out = {

            "file_id": file_id,

            "tank_id":
                row["tank_id"],

            "label":
                row["binary_label"]
        }

        out.update(
            feat
        )

        write_header = (
            not os.path.exists(
                OUTPUT_CSV
            )
        )

        pd.DataFrame(
            [out]
        ).to_csv(
            OUTPUT_CSV,
            mode="a",
            index=False,
            header=write_header
        )

        processed_this_run += 1

        if processed_this_run % 25 == 0:

            print(
                f"Processed {processed_this_run}"
            )

    except Exception as e:

        try:
            os.remove(wav_file)
        except:
            pass

        print(
            f"FAILED {file_id}"
        )

        print(e)

print(
    "\nRUN COMPLETE"
)
