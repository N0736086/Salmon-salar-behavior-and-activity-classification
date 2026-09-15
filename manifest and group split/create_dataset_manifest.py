import os
import re
import pandas as pd

# =====================================================
# CONFIGURATION
# =====================================================

DATASET_ROOT = (
    "/media/feliciano/Aux/AI_AFS_DATASET/"
    "AFS_BEHAVIOUR_DATASET"
)

METADATA_FILE = (
    "/home/feliciano/METADATA_BOX/"
    "download_metadata.csv"
)

OUTPUT_MANIFEST = "dataset_manifest.csv"

CLASSES = [
    "normal",
    "clustering",
    "agitation",
    "other"
]

# =====================================================
# LOAD RECORDING METADATA
# =====================================================

meta = pd.read_csv(
    METADATA_FILE
)

meta["recording_start_time"] = pd.to_datetime(
    meta["recording_start_time"]
)

#
# All parent WAV files are 10 minutes
#

meta["recording_end_time"] = (
    meta["recording_start_time"]
    + pd.Timedelta(minutes=10)
)

print("\nMetadata loaded")
print(
    "Parent recordings:",
    len(meta)
)

# =====================================================
# BUILD MANIFEST
# =====================================================

rows = []

matched = 0
unmatched = 0

for label in CLASSES:

    class_dir = os.path.join(
        DATASET_ROOT,
        label
    )

    files = sorted([
        f
        for f in os.listdir(class_dir)
        if f.lower().endswith(".wav")
    ])

    print(
        f"{label}: {len(files)} clips"
    )

    for wav_file in files:

        try:

            clip_timestamp = pd.to_datetime(
                wav_file.replace(".wav", ""),
                format="%Y%m%d_%H%M%S"
            )

            parent = meta[
                (
                    meta["recording_start_time"]
                    <= clip_timestamp
                )
                &
                (
                    meta["recording_end_time"]
                    > clip_timestamp
                )
            ]

            if len(parent) == 0:

                unmatched += 1
                continue

            parent = parent.iloc[0]

            #
            # Extract tank from parent path
            #

            parent_path = str(
                parent["parent_file_path"]
            )

            tank_match = re.search(
                r"Tank[_ ]?(\d+)",
                parent_path,
                flags=re.IGNORECASE
            )

            if tank_match:

                tank_id = (
                    f"Tank{tank_match.group(1)}"
                )

            else:

                tank_id = "UNKNOWN"

            rows.append({

                "clip_path":
                    os.path.join(
                        class_dir,
                        wav_file
                    ),

                "label":
                    label,

                "filename":
                    wav_file,

                "clip_timestamp":
                    clip_timestamp,

                "parent_file_id":
                    parent["parent_file_id"],

                "parent_file_name":
                    parent["parent_file_name"],

                "parent_file_path":
                    parent["parent_file_path"],

                "tank_id":
                    tank_id,

                "session_id":
                    str(
                        parent["session_id"]
                    ),

                "recording_start_time":
                    parent["recording_start_time"],

                "recording_end_time":
                    parent["recording_end_time"]
            })

            matched += 1

        except Exception as e:

            unmatched += 1

            print(
                "ERROR:",
                wav_file,
                e
            )

# =====================================================
# SAVE
# =====================================================

manifest = pd.DataFrame(rows)

print("\n================================")
print("MANIFEST SUMMARY")
print("================================")

print(
    "Matched clips:",
    matched
)

print(
    "Unmatched clips:",
    unmatched
)

print(
    "Total clips:",
    len(manifest)
)

print(
    "Unique parent recordings:",
    manifest["parent_file_id"].nunique()
)

print()
print("Tank distribution")

print(
    manifest["tank_id"]
    .value_counts(dropna=False)
)

manifest.to_csv(
    OUTPUT_MANIFEST,
    index=False
)

print()
print(
    f"Saved: {OUTPUT_MANIFEST}"
)
