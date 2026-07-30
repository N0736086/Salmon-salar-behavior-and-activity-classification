#!/usr/bin/env python3

import pandas as pd

ETHOGRAM = (
    "metadata_downloads/"
    "2199077307694_001128 - AI-AFS- datasheet - ethogram -  2025 - VE.xlsx"
)

LABEL_MAP = {
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

frames = []

for sheet in ["Routine", "Intervenants", "Poissons"]:

    print(f"Processing {sheet}")

    df = pd.read_excel(
        ETHOGRAM,
        sheet_name=sheet,
        engine="openpyxl"
    )

    headers = []
    seen = {}

    for value in df.iloc[0].tolist():

        col = str(value).strip()

        if col == "nan":
            col = "empty"

        if col in seen:
            seen[col] += 1
            col = f"{col}_{seen[col]}"
        else:
            seen[col] = 0

        headers.append(col)

    data = df.iloc[1:].copy()

    data.columns = headers

    data["source"] = sheet.lower()

    if "Code" in data.columns:

        data["label"] = (
            data["Code"]
            .astype(str)
            .str.strip()
            .map(LABEL_MAP)
        )

    else:

        data["label"] = None

    frames.append(data)

ethogram = pd.concat(
    frames,
    ignore_index=True,
    sort=False
)

ethogram.to_csv(
    "ethogram_clean.csv",
    index=False
)

print("\nSaved: ethogram_clean.csv")
print("\nRows:", len(ethogram))
print("\nColumns:")

for c in ethogram.columns:
    print(c)

print("\nLabel counts:")
print(
    ethogram["label"]
    .value_counts(dropna=False)
)
