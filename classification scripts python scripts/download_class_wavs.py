import os
import pandas as pd
import requests

TOKEN = "JpknrmY0D5pJ8xN21NPdQWVB17hJAHBU"

manifest = pd.read_csv(
    "download_manifest.csv",
    dtype={"file_id": str}
)

BASE = os.path.expanduser(
    "~/feeding_dataset"
)

folders = {
    0: "Class_0_Background",
    1: "Class_1_PreFeeding",
    2: "Class_2_Feeding",
    3: "Class_3_PostFeeding",
}

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

for _, row in manifest.iterrows():

    file_id = row["file_id"]

    cls = int(row["class"])

    target_dir = os.path.join(
        BASE,
        folders[cls]
    )

    os.makedirs(
        target_dir,
        exist_ok=True
    )

    filename = row["file_name"]

    out_file = os.path.join(
        target_dir,
        filename
    )

    if os.path.exists(out_file):
        continue

    try:

        url = (
            f"https://api.box.com/2.0/files/"
            f"{file_id}/content"
        )

        r = requests.get(
            url,
            headers=headers,
            stream=True,
            allow_redirects=True
        )

        r.raise_for_status()

        with open(
            out_file,
            "wb"
        ) as f:

            for chunk in r.iter_content(
                1024 * 1024
            ):

                if chunk:
                    f.write(chunk)

        print(
            "Downloaded:",
            filename
        )

    except Exception as e:

        print(
            "FAILED:",
            filename,
            e
        )
