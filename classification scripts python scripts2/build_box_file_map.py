# build_box_file_map.py

import requests
import pandas as pd

TOKEN = "7OlKbASEdbXXu8ZGMLBAqneL3im1DBsw"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

rows = []


def walk_folder(folder_id, current_path=""):

    url = (
        f"https://api.box.com/2.0/folders/"
        f"{folder_id}/items"
        "?limit=1000"
    )

    r = requests.get(
        url,
        headers=headers
    )

    r.raise_for_status()

    items = r.json()["entries"]

    for item in items:

        name = item["name"]

        path = f"{current_path}/{name}"

        if item["type"] == "file":

            rows.append({
                "file_id": item["id"],
                "file_name": item["name"],
                "path": path
            })

        elif item["type"] == "folder":

            print("FOLDER:", path)

            walk_folder(
                item["id"],
                path
            )


# ROOT FOLDER
walk_folder("0")

df = pd.DataFrame(rows)

df.to_csv(
    "box_file_map.csv",
    index=False
)

print()
print("FILES:", len(df))
print("Saved box_file_map.csv")
