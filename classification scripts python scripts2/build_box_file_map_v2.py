# build_box_file_map_v2.py

import requests
import pandas as pd
import time

TOKEN = "T5i0pNyGt3VUnMnsXdn7CCpYxpAvNMdz"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

rows = []
failed = []


def walk(folder_id, path=""):

    url = (
        f"https://api.box.com/2.0/folders/"
        f"{folder_id}/items"
        "?limit=1000"
    )

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=60
    )

    if r.status_code != 200:

        failed.append({
            "folder_id": folder_id,
            "path": path,
            "status": r.status_code,
            "error": r.text
        })

        print(
            f"FAILED {folder_id} {r.status_code}"
        )

        return

    data = r.json()

    for item in data["entries"]:

        item_path = (
            path + "/" + item["name"]
        )

        if item["type"] == "file":

            rows.append({
                "file_id": item["id"],
                "file_name": item["name"],
                "path": item_path
            })

        elif item["type"] == "folder":

            print("FOLDER:", item_path)

            try:

                walk(
                    item["id"],
                    item_path
                )

            except Exception as e:

                failed.append({
                    "folder_id": item["id"],
                    "path": item_path,
                    "status": "EXCEPTION",
                    "error": str(e)
                })

                continue


walk("0")

pd.DataFrame(rows).to_csv(
    "box_file_map.csv",
    index=False
)

pd.DataFrame(failed).to_csv(
    "box_failed_folders.csv",
    index=False
)

print()
print("FILES FOUND:", len(rows))
print("FAILED:", len(failed))
