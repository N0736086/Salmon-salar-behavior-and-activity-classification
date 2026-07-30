from box_sdk_gen import *
import pandas as pd

TOKEN = "NLidSRiNdSVkq5PiXLvftGQy92DnYMp9"

ROOT_FOLDER = "353082741274"

auth = BoxDeveloperTokenAuth(TOKEN)
client = BoxClient(auth)

records = []

def scan(folder_id, path=""):

    offset = 0
    limit = 1000

    while True:

        result = client.folders.get_folder_items(
            folder_id,
            limit=limit,
            offset=offset
        )

        if len(result.entries) == 0:
            break

        for item in result.entries:

            item_path = f"{path}/{item.name}"

            print(item_path)

            records.append({
                "id": item.id,
                "name": item.name,
                "type": str(item.type),
                "path": item_path
            })

            if str(item.type).endswith("FOLDER"):
                scan(item.id, item_path)

        offset += limit

scan(ROOT_FOLDER)

df = pd.DataFrame(records)

df.to_csv(
    "box_inventory.csv",
    index=False
)

print(f"Found {len(df)} items")
