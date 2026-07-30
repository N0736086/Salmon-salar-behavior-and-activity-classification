#!/usr/bin/env python3

import os
import pandas as pd

FOLDER = "metadata_downloads"

print("\nInspecting Excel files...\n")

for file in os.listdir(FOLDER):

    if not file.endswith(".xlsx"):
        continue

    path = os.path.join(FOLDER, file)

    print("=" * 80)
    print(file)
    print("=" * 80)

    try:

        xls = pd.ExcelFile(path)

        print("\nSheets:")

        for sheet in xls.sheet_names:

            print(f"  - {sheet}")

            try:

                df = pd.read_excel(
                    path,
                    sheet_name=sheet,
                    nrows=5
                )

                print("\nColumns:")
                print(list(df.columns))

                print("\nPreview:")
                print(df.head())

            except Exception as e:

                print(
                    f"Could not read sheet {sheet}"
                )
                print(e)

            print("\n")

    except Exception as e:

        print(
            f"ERROR opening {file}"
        )
        print(e)

print("\nFinished.")
