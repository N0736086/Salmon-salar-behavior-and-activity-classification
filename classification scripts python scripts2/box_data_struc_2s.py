from boxsdk import Client, OAuth2
from pathlib import Path
from datetime import datetime, timedelta
import soundfile as sf
import pandas as pd
import numpy as np
import csv
import re
import os
import tempfile

# =====================================================
# CONFIG
# =====================================================

BOX_TOKEN = "JyL4jA1JVdli88FlcZlpKZilWHqH2ner"

BOX_ROOT_FOLDER_ID = "0"

ETHOGRAM_CSV = "feeding_intervals.csv"

OUTPUT_ROOT = "/media/feliciano/Aux/AI_AFS_DATASET/segmented_2s"

SEGMENT_DURATION = 2

# =====================================================
# BOX LOGIN
# =====================================================

auth = OAuth2(
    client_id=None,
    client_secret=None,
    access_token=BOX_TOKEN
)

client = Client(auth)

# =====================================================
# LOAD ETHOGRAM
# =====================================================

ethogram = pd.read_csv(ETHOGRAM_CSV)

ethogram["start"] = pd.to_datetime(
    ethogram["date"] + " " + ethogram["start_time"]
)

ethogram["end"] = pd.to_datetime(
    ethogram["date"] + " " + ethogram["end_time"]
)

# =====================================================
# HELPERS
# =====================================================

def extract_timestamp(filename):

    m = re.search(
        r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})",
        filename
    )

    if not m:
        return None

    return datetime.strptime(
        m.group(1),
        "%Y-%m-%d_%H-%M-%S"
    )


def overlaps_ethogram(record_start,
                      record_end):

    for _, row in ethogram.iterrows():

        if (
            row["start"] < record_end
            and
            row["end"] > record_start
        ):
            return True

    return False


# =====================================================
# METADATA
# =====================================================

metadata = []

# =====================================================
# SEGMENT FILE
# =====================================================

def segment_file(
    wav_path,
    relative_folder,
    parent_file_name
):

    audio, sr = sf.read(wav_path)

    if len(audio.shape) > 1:
        audio = np.mean(
            audio,
            axis=1
        )

    start_ts = extract_timestamp(
        parent_file_name
    )

    if start_ts is None:
        print(
            "No timestamp:",
            parent_file_name
        )
        return

    samples_per_segment = (
        sr * SEGMENT_DURATION
    )

    n_segments = (
        len(audio)
        // samples_per_segment
    )

    output_folder = (
        Path(OUTPUT_ROOT)
        / relative_folder
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    for i in range(n_segments):

        s = i * samples_per_segment
        e = s + samples_per_segment

        seg = audio[s:e]

        seg_time = (
            start_ts
            +
            timedelta(
                seconds=i * SEGMENT_DURATION
            )
        )

        name = (
            seg_time.strftime(
                "%Y-%m-%d_%H-%M-%S"
            )
            +
            ".wav"
        )

        out_file = (
            output_folder
            / name
        )

        sf.write(
            out_file,
            seg,
            sr
        )

        metadata.append([
            str(out_file),
            parent_file_name,
            seg_time.isoformat(),
            str(relative_folder)
        ])


# =====================================================
# TRAVERSE BOX
# =====================================================

def process_folder(
    folder_id,
    relative_path=""
):

    folder = client.folder(folder_id)

    items = folder.get_items()

    for item in items:

        if item.type == "folder":

            process_folder(
                item.id,
                os.path.join(
                    relative_path,
                    item.name
                )
            )

        elif item.type == "file":

            if not item.name.lower().endswith(
                ".wav"
            ):
                continue

            start_ts = extract_timestamp(
                item.name
            )

            if start_ts is None:
                continue

            #
            # IMPORTANT
            #
            # Replace with actual duration extraction
            # from metadata if duration known.
            #

            assumed_duration_sec = 600

            end_ts = (
                start_ts
                +
                timedelta(
                    seconds=
                    assumed_duration_sec
                )
            )

            if not overlaps_ethogram(
                start_ts,
                end_ts
            ):
                continue

            print(
                "Downloading:",
                item.name
            )

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp:

                item.download_to(
                    temp
                )

                temp_path = temp.name

            segment_file(
                temp_path,
                relative_path,
                item.name
            )

            os.remove(
                temp_path
            )

# =====================================================
# RUN
# =====================================================

process_folder(
    BOX_ROOT_FOLDER_ID
)

# =====================================================
# SAVE INDEX
# =====================================================

with open(
    "segment_index.csv",
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "segment_file",
        "parent_file",
        "timestamp",
        "folder"
    ])

    writer.writerows(metadata)

print(
    "Finished:",
    len(metadata),
    "segments"
)
