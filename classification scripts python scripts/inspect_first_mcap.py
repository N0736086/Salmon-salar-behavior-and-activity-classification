import os
import tempfile
import requests
import pandas as pd

from mcap.reader import make_reader

TOKEN = "fxG8qkF57nCIN2yTcFFV7Kr0rJj5Ilrp"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# -----------------------------------------
# Find first MCAP in Box inventory
# -----------------------------------------

df = pd.read_csv("box_file_map.csv")

mcap = df[
    df["file_name"]
    .str.lower()
    .str.endswith(".mcap", na=False)
]

if len(mcap) == 0:

    print("No MCAP files found.")

    raise SystemExit

row = mcap.iloc[0]

file_id = str(row["file_id"])

print("MCAP:")
print(row["file_name"])
print("File ID:", file_id)

# -----------------------------------------
# Download ONE MCAP
# -----------------------------------------

url = f"https://api.box.com/2.0/files/{file_id}/content"

r = requests.get(
    url,
    headers=HEADERS,
    stream=True,
    allow_redirects=True,
    timeout=300
)

r.raise_for_status()

tmp = tempfile.NamedTemporaryFile(
    suffix=".mcap",
    delete=False
)

for chunk in r.iter_content(
    chunk_size=1024 * 1024
):
    if chunk:
        tmp.write(chunk)

tmp.close()

# -----------------------------------------
# Inspect topics
# -----------------------------------------

topics = set()

with open(tmp.name, "rb") as f:

    reader = make_reader(f)

    for schema, channel, message in reader.iter_messages():

        topics.add(channel.topic)

print("\nTOPICS\n")

for t in sorted(topics):
    print(t)

# -----------------------------------------
# Delete temp MCAP
# -----------------------------------------

os.remove(tmp.name)

print("\nTemporary MCAP removed.")
