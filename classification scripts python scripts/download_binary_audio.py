#!/usr/bin/env python3

import os
import pandas as pd

from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth
)

# ==========================================
# CONFIG
# ==========================================

TOKEN = "Tl9wyG20XkY0gtyg1J92RyCmV49dyal3"

MANIFEST = "binary_manifest.csv"

OUTPUT_DIR = "binary_audio"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==========================================
# BOX
# ==========================================

auth = BoxDeveloperTokenAuth(TOKEN)

client = BoxClient(auth)

# ==========================================
# FILES
# ==========================================

df = pd.read_csv(
    MANIFEST
)

# ==========================================
# DOWNLOAD
# ==========================================

for idx, row in df.iterrows():

    file_id = str(
        row["file_id"]
    )

    filename = (
        row["file_name"]
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        filename
    )

    if os.path.exists(
        output_file
    ):

        print(
            f"SKIP {filename}"
        )

        continue

    print(
        f"{idx+1}/{len(df)}  {filename}"
    )

    try:

        stream = (
            client.downloads
            .download_file(
                file_id
            )
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

    except Exception as e:

        print(
            "FAILED:",
            filename
        )

        print(e)

print("\nFinished.")
