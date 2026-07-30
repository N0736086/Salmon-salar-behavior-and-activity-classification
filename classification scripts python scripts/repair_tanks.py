#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("training_manifest.csv")

mapping = {
    "LUW1698": "tank1",
    "LUW6548": "tank2",
    "LUW7168": "tank3",
    "LUW7169": "tank4",
}

def repair_tank(row):

    if pd.notna(row["tank"]) and row["tank"] != "unknown":
        return row["tank"]

    name = str(row["file_name"])

    for prefix, tank in mapping.items():

        if name.startswith(prefix):
            return tank

    return row["tank"]

df["tank"] = df.apply(
    repair_tank,
    axis=1
)

tank_type_map = {
    "tank1": "control",
    "tank2": "experimental",
    "tank3": "experimental",
    "tank4": "experimental",
}

df["tank_type"] = (
    df["tank"]
    .map(tank_type_map)
)

df.to_csv(
    "training_manifest_fixed.csv",
    index=False
)

print(df["tank"].value_counts())
