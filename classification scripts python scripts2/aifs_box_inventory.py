#!/usr/bin/env python3

import os
import re
import pandas as pd
from pathlib import Path

from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth
)

# =====================================================
# CONFIGURATION
# =====================================================

TOKEN = "NLidSRiNdSVkq5PiXLvftGQy92DnYMp9"

ROOT_FOLDER_ID = "353082741274"

OUTPUT_DIR = "aifs_inventory"

# =====================================================
# SETUP
# =====================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

auth = BoxDeveloperTokenAuth(TOKEN)

client = BoxClient(auth)

print("Connected to Box")

# =====================================================
# REPOSITORY INVENTORY
# =====================================================

inventory = []

def scan_folder(folder_id, path=""):

    offset = 0
    limit = 1000

    while True:

        response = client.folders.get_folder_items(
            folder_id,
            limit=limit,
            offset=offset
        )

        if len(response.entries) == 0:
            break

        for item in response.entries:

            item_path = f"{path}/{item.name}"

            print(item_path)

            inventory.append({
                "id": item.id,
                "name": item.name,
                "type": item.type.value,
                "path": item_path
            })

            if item.type.value == "folder":

                scan_folder(
                    item.id,
                    item_path
                )

        offset += limit


print("Scanning repository ...")

scan_folder(ROOT_FOLDER_ID)

inventory_df = pd.DataFrame(inventory)

inventory_csv = (
    f"{OUTPUT_DIR}/box_inventory.csv"
)

inventory_df.to_csv(
    inventory_csv,
    index=False
)

print()
print("Inventory saved:")
print(inventory_csv)

print(
    "Total items:",
    len(inventory_df)
)

# =====================================================
# IDENTIFY DATA TYPES
# =====================================================

audio_pattern = (
    r"\.(wav|flac|mp3|m4a)$"
)

video_pattern = (
    r"\.(mcap|mp4|avi|mov)$"
)

excel_pattern = (
    r"\.(xlsx|xls|csv)$"
)

audio_df = inventory_df[
    inventory_df["name"].str.contains(
        audio_pattern,
        case=False,
        na=False,
        regex=True
    )
]

video_df = inventory_df[
    inventory_df["name"].str.contains(
        video_pattern,
        case=False,
        na=False,
        regex=True
    )
]

metadata_df = inventory_df[
    inventory_df["name"].str.contains(
        excel_pattern,
        case=False,
        na=False,
        regex=True
    )
]

audio_df.to_csv(
    f"{OUTPUT_DIR}/audio_inventory.csv",
    index=False
)

video_df.to_csv(
    f"{OUTPUT_DIR}/video_inventory.csv",
    index=False
)

metadata_df.to_csv(
    f"{OUTPUT_DIR}/metadata_inventory.csv",
    index=False
)

print()
print("Audio files:", len(audio_df))
print("Video files:", len(video_df))
print("Metadata files:", len(metadata_df))

# =====================================================
# DETECT TANK
# =====================================================

def detect_tank(path):

    p = path.lower()

    if "tank1" in p:
        return "tank1"

    if "tank2" in p:
        return "tank2"

    if "tank3" in p:
        return "tank3"

    if "tank4" in p:
        return "tank4"

    return "unknown"


def detect_tank_type(path):

    tank = detect_tank(path)

    if tank == "tank1":
        return "control"

    if tank in [
        "tank2",
        "tank3",
        "tank4"
    ]:
        return "experimental"

    return "unknown"


inventory_df["tank"] = (
    inventory_df["path"]
    .apply(detect_tank)
)

inventory_df["tank_type"] = (
    inventory_df["path"]
    .apply(detect_tank_type)
)

inventory_df.to_csv(
    f"{OUTPUT_DIR}/inventory_with_tanks.csv",
    index=False
)

# =====================================================
# EXTRACT TIMESTAMPS
# =====================================================

def extract_timestamp(name):

    patterns = [

        r"(\d{8})_(\d{6})_(\d+)",

        r"(\d{8})_(\d{6})"

    ]

    for pattern in patterns:

        m = re.search(
            pattern,
            name
        )

        if m:

            if len(m.groups()) >= 2:

                return (
                    f"{m.group(1)}_"
                    f"{m.group(2)}"
                )

    return None


inventory_df["timestamp"] = (
    inventory_df["name"]
    .apply(extract_timestamp)
)

inventory_df.to_csv(
    f"{OUTPUT_DIR}/inventory_with_time.csv",
    index=False
)

# =====================================================
# DOWNLOAD ONLY METADATA
# =====================================================

metadata_download_dir = (
    f"{OUTPUT_DIR}/metadata"
)

os.makedirs(
    metadata_download_dir,
    exist_ok=True
)

print()
print(
    "Downloading metadata files only..."
)

for _, row in metadata_df.iterrows():

    try:

        filename = row["name"]

        target = os.path.join(
            metadata_download_dir,
            filename
        )

        if os.path.exists(target):
            continue

        print(
            "Downloading:",
            filename
        )

        with open(
            target,
            "wb"
        ) as f:

            client.downloads.download_file(
                row["id"],
                f
            )

    except Exception as e:

        print(
            "Failed:",
            row["name"],
            e
        )

# =====================================================
# AI-AFS MASTER MANIFEST
# =====================================================

manifest = inventory_df[
    inventory_df["tank"] != "unknown"
].copy()

manifest = manifest[
    [
        "id",
        "name",
        "path",
        "tank",
        "tank_type",
        "timestamp",
        "type"
    ]
]

manifest.to_csv(
    f"{OUTPUT_DIR}/aifs_master_manifest.csv",
    index=False
)

print()
print(
    "AI-AFS manifest created:"
)

print(
    f"{OUTPUT_DIR}/aifs_master_manifest.csv"
)

print()
print("FINISHED")
