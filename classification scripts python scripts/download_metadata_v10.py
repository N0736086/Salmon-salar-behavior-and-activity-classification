#!/usr/bin/env python3

import os
import pandas as pd

from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth
)

# ============================================================
# CONFIGURATION
# ============================================================

TOKEN = "5N0KeaibWHODzEKVEG2tOzia1PD6WLNs"

METADATA_CSV = (
    "aifs_inventory/metadata_inventory.csv"
)

OUTPUT_DIR = "metadata_downloads"

# ============================================================
# AUTHENTICATION
# ============================================================

print("Connecting to Box...")

auth = BoxDeveloperTokenAuth(TOKEN)

client = BoxClient(auth)

me = client.users.get_user_me()

print(f"Connected as: {me.name}")
print(f"Email       : {me.login}")

# ============================================================
# OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ============================================================
# LOAD METADATA INVENTORY
# ============================================================

if not os.path.exists(METADATA_CSV):

    raise FileNotFoundError(
        f"Cannot find {METADATA_CSV}"
    )

df = pd.read_csv(METADATA_CSV)

print("\nMetadata files discovered:")
print(df[["id", "name"]])

# ============================================================
# OPTIONAL FILTER
# Only download files relevant to AI-AFS
# ============================================================

target_df = df[
    df["name"].str.contains(
        r"ethogram|salmon|saumon|water|eau",
        case=False,
        na=False,
        regex=True
    )
]

print(
    f"\nFiles selected for download: {len(target_df)}"
)

# ============================================================
# DOWNLOAD
# ============================================================

download_log = []

for _, row in target_df.iterrows():

    file_id = str(row["id"])
    filename = str(row["name"])

    # avoid overwriting duplicates
    output_file = os.path.join(
        OUTPUT_DIR,
        f"{file_id}_{filename}"
    )

    if os.path.exists(output_file):

        print(
            f"SKIP: {filename}"
        )

        download_log.append({
            "id": file_id,
            "file": filename,
            "status": "already_exists"
        })

        continue

    print(
        f"\nDownloading: {filename}"
    )

    try:

        stream = client.downloads.download_file(
            file_id
        )

        with open(
            output_file,
            "wb"
        ) as f:

            while True:

                chunk = stream.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                f.write(chunk)

        size_mb = (
            os.path.getsize(output_file)
            / 1024
            / 1024
        )

        print(
            f"OK -> {output_file}"
        )

        print(
            f"Size: {size_mb:.2f} MB"
        )

        download_log.append({
            "id": file_id,
            "file": filename,
            "status": "downloaded"
        })

    except Exception as e:

        print(
            f"FAILED -> {filename}"
        )

        print(e)

        download_log.append({
            "id": file_id,
            "file": filename,
            "status": f"failed: {e}"
        })

# ============================================================
# SAVE LOG
# ============================================================

log_df = pd.DataFrame(
    download_log
)

log_path = os.path.join(
    OUTPUT_DIR,
    "download_log.csv"
)

log_df.to_csv(
    log_path,
    index=False
)

print("\n===================================================")
print("DOWNLOAD SUMMARY")
print("===================================================")

print(
    log_df["status"]
    .value_counts(dropna=False)
)

print(
    f"\nLog saved to: {log_path}"
)

print("\nFinished.")
