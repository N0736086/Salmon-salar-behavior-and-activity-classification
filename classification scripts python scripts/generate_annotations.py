#!/usr/bin/env python3

import pandas as pd
import re
from pathlib import Path

# =====================================================
# FIND ETHOGRAM FILE
# =====================================================

files = list(
    Path("metadata_downloads").glob(
        "*ethogram*.xlsx"
    )
)

if len(files) == 0:
    raise FileNotFoundError(
        "No ethogram file found in metadata_downloads"
    )

ETHOGRAM_FILE = files[0]

print("Using:", ETHOGRAM_FILE)

AUDIO_FILE = (
    "aifs_inventory/audio_inventory.csv"
)

# =====================================================
# LOAD SHEET
# =====================================================

def clean_sheet(sheet_name, source):

    raw = pd.read_excel(
        ETHOGRAM_FILE,
        sheet_name=sheet_name,
        header=None,
        engine="openpyxl"
    )

    headers = raw.iloc[0]

    df = raw.iloc[1:].copy()

    df.columns = headers

    df["source"] = source

    return df

# =====================================================
# ETHOGRAM
# =====================================================

routine = clean_sheet(
    "Routine",
    "routine"
)

intervenants = clean_sheet(
    "Intervenants",
    "intervenants"
)

poissons = clean_sheet(
    "Poissons",
    "poissons"
)

ethogram = pd.concat(
    [
        routine,
        intervenants,
        poissons
    ],
    ignore_index=True
)

# =====================================================
# FIND CODE COLUMN
# =====================================================

code_column = None

for col in ethogram.columns:

    if str(col).strip().lower() == "code":

        code_column = col
        break

print("Code column:", code_column)

# =====================================================
# LABEL MAP
# =====================================================

label_map = {

    "R1": "visual_check",
    "R2": "feeding",
    "R3": "routine_operation",
    "R4": "cleaning",
    "R5": "handling",
    "R6": "maintenance",

    "E1": "simple_passage",
    "E2": "technical_intervention",

    "P1": "normal_activity"
}

if code_column:

    ethogram["label"] = (
        ethogram[code_column]
        .astype(str)
        .str.strip()
        .map(label_map)
    )

else:

    ethogram["label"] = "unknown"

# =====================================================
# SAVE ETHOGRAM
# =====================================================

ethogram.to_csv(
    "ethogram_clean.csv",
    index=False
)

print(
    "Created ethogram_clean.csv"
)

# =====================================================
# AUDIO INVENTORY
# =====================================================

audio = pd.read_csv(
    AUDIO_FILE
)

# =====================================================
# TIMESTAMP EXTRACTION
# =====================================================

def extract_timestamp(filename):

    filename = str(filename)

    m = re.search(
        r"(\d{8})_(\d{6})",
        filename
    )

    if not m:
        return pd.NaT

    try:

        return pd.to_datetime(
            m.group(1) + m.group(2),
            format="%Y%m%d%H%M%S"
        )

    except:
        return pd.NaT

audio["audio_timestamp"] = (
    audio["name"]
    .apply(extract_timestamp)
)

# =====================================================
# TANK DETECTION
# =====================================================

def detect_tank(path):

    path = str(path).lower()

    if "tank1" in path:
        return "tank1"

    if "tank2" in path:
        return "tank2"

    if "tank3" in path:
        return "tank3"

    if "tank4" in path:
        return "tank4"

    return "unknown"

audio["tank"] = (
    audio["path"]
    .apply(detect_tank)
)

audio["tank_type"] = (
    audio["tank"]
    .map({
        "tank1": "control",
        "tank2": "experimental",
        "tank3": "experimental",
        "tank4": "experimental"
    })
)

# =====================================================
# MASTER ANNOTATIONS
# =====================================================

master = audio.copy()

master.to_csv(
    "master_annotations.csv",
    index=False
)

print(
    "Created master_annotations.csv"
)

print(
    "Ethogram rows:",
    len(ethogram)
)

print(
    "Audio rows:",
    len(master)
)
