#!/usr/bin/env python3

import os
import soundfile as sf
import pandas as pd

INPUT_DIR = "binary_audio"
OUTPUT_DIR = "segments"

os.makedirs(OUTPUT_DIR, exist_ok=True)

manifest = pd.read_csv("binary_manifest.csv")

rows = []

SEGMENT_SECONDS = 5

for _, row in manifest.iterrows():

    wav_file = os.path.join(
        INPUT_DIR,
        row["file_name"]
    )

    if not os.path.exists(wav_file):
        continue

    print("Processing:", row["file_name"])

    try:

        audio, sr = sf.read(wav_file)

        samples_per_segment = (
            SEGMENT_SECONDS * sr
        )

        n_segments = (
            len(audio)
            //
            samples_per_segment
        )

        label_dir = os.path.join(
            OUTPUT_DIR,
            row["protocol_label"]
        )

        os.makedirs(
            label_dir,
            exist_ok=True
        )

        for i in range(n_segments):

            start = (
                i
                * samples_per_segment
            )

            end = (
                start
                + samples_per_segment
            )

            segment = audio[start:end]

            out_name = (
                f"{row['file_id']}_seg{i}.wav"
            )

            out_path = os.path.join(
                label_dir,
                out_name
            )

            sf.write(
                out_path,
                segment,
                sr
            )

            rows.append(
                {
                    "segment_file": out_name,
                    "label": row["protocol_label"],
                    "tank": row["tank"],
                    "file_id": row["file_id"]
                }
            )

    except Exception as e:

        print(
            "FAILED:",
            row["file_name"]
        )

        print(e)

segments = pd.DataFrame(rows)

segments.to_csv(
    "segment_manifest.csv",
    index=False
)

print(
    "\nSegments created:",
    len(segments)
)

