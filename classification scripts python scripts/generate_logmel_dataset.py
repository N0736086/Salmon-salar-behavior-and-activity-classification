#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd

import librosa
import librosa.display

import matplotlib.pyplot as plt

from pathlib import Path

SEGMENT_ROOT = "segments"
OUTPUT_ROOT = "logmel"

SR = 8000
N_MELS = 128
N_FFT = 1024
HOP_LENGTH = 256

manifest = pd.read_csv(
    "segment_manifest.csv"
)

os.makedirs(
    OUTPUT_ROOT,
    exist_ok=True
)

count = 0

for _, row in manifest.iterrows():

    segment_name = row["segment_file"]

    label = row["label"]

    matches = list(
        Path(SEGMENT_ROOT)
        .rglob(segment_name)
    )

    if len(matches) == 0:
        continue

    wav_path = str(matches[0])

    try:

        y, sr = librosa.load(
            wav_path,
            sr=SR
        )

        mel = librosa.feature.melspectrogram(
            y=y,
            sr=sr,
            n_mels=N_MELS,
            n_fft=N_FFT,
            hop_length=HOP_LENGTH
        )

        mel_db = librosa.power_to_db(
            mel,
            ref=np.max
        )

        out_dir = os.path.join(
            OUTPUT_ROOT,
            label
        )

        os.makedirs(
            out_dir,
            exist_ok=True
        )

        out_file = os.path.join(
            out_dir,
            segment_name.replace(
                ".wav",
                ".png"
            )
        )

        plt.figure(
            figsize=(4, 4)
        )

        librosa.display.specshow(
            mel_db,
            sr=sr,
            hop_length=HOP_LENGTH
        )

        plt.axis("off")

        plt.savefig(
            out_file,
            bbox_inches="tight",
            pad_inches=0
        )

        plt.close()

        count += 1

        if count % 1000 == 0:

            print(
                f"Generated {count}"
            )

    except Exception as e:

        print(
            f"FAILED {segment_name}"
        )

print(
    f"\nCompleted: {count}"
)
