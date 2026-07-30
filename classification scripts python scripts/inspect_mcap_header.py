# inspect_mcap_header.py

import tempfile
import requests
import pandas as pd

TOKEN = "fxG8qkF57nCIN2yTcFFV7Kr0rJj5Ilrp"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

df = pd.read_csv("box_file_map.csv")

mcap = df[
    df["file_name"]
    .str.lower()
    .str.endswith(".mcap", na=False)
]

row = mcap.iloc[0]

file_id = str(row["file_id"])

print("FILE:", row["file_name"])
print("ID:", file_id)

url = f"https://api.box.com/2.0/files/{file_id}/content"

r = requests.get(
    url,
    headers=HEADERS,
    allow_redirects=True,
    timeout=300
)

print("STATUS:", r.status_code)

print("\nFIRST 64 BYTES\n")

print(r.content[:64])

print("\nFIRST 16 HEX BYTES\n")

print(r.content[:16].hex())

