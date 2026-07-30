import pandas as pd
import re

audio = pd.read_csv(
    "aifs_inventory/audio_inventory.csv"
)

ethogram = pd.read_csv(
    "ethogram_clean.csv"
)

#
# extract timestamp from filename
#

def get_time(fname):

    fname = str(fname)

    m = re.search(
        r'(\d{8})_(\d{6})',
        fname
    )

    if not m:
        return pd.NaT

    return pd.to_datetime(
        m.group(1) + m.group(2),
        format="%Y%m%d%H%M%S",
        errors="coerce"
    )

audio["timestamp"] = (
    audio["name"]
    .apply(get_time)
)

#
# tank extraction
#

def tank(path):

    p = str(path).lower()

    if "tank1" in p:
        return "tank1"

    if "tank2" in p:
        return "tank2"

    if "tank3" in p:
        return "tank3"

    if "tank4" in p:
        return "tank4"

    return "unknown"

audio["tank"] = (
    audio["path"]
    .apply(tank)
)

audio["tank_type"] = (
    audio["tank"]
    .map({
        "tank1":"control",
        "tank2":"experimental",
        "tank3":"experimental",
        "tank4":"experimental"
    })
)

master = audio[
    [
        "id",
        "name",
        "path",
        "tank",
        "tank_type",
        "timestamp"
    ]
].copy()

master.columns = [
    "file_id",
    "file_name",
    "path",
    "tank",
    "tank_type",
    "timestamp"
]

master.to_csv(
    "master_annotations.csv",
    index=False
)

print(
    "Saved master_annotations.csv"
)

print(master.head())
print()
print("Rows:", len(master))
