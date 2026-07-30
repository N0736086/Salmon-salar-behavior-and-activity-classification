import os
import tempfile
import requests
import pandas as pd
import re

TOKEN = "fxG8qkF57nCIN2yTcFFV7Kr0rJj5Ilrp"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# First MCAP from inventory
df = pd.read_csv("box_file_map.csv")

mcap = df[
    df["file_name"]
    .str.lower()
    .str.endswith(".mcap", na=False)
]

row = mcap.iloc[0]

file_id = str(row["file_id"])

print("FILE:", row["file_name"])
print("FILE_ID:", file_id)

# Download one MCAP
url = f"https://api.box.com/2.0/files/{file_id}/content"

r = requests.get(
    url,
    headers=HEADERS,
    stream=True,
    allow_redirects=True
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

print("LOCAL:", tmp.name)

# Read binary
with open(tmp.name, "rb") as f:
    data = f.read()

# Extract printable strings
strings = re.findall(
    rb"[\x20-\x7E]{4,}",
    data
)

strings = [
    s.decode(
        "utf-8",
        errors="ignore"
    )
    for s in strings
]

# Look for ROS topics
print("\nPOSSIBLE TOPICS\n")

for s in strings:

    if "/" in s:

        if len(s) < 200:

            print(s)

# Look for audio-related words
print("\nAUDIO CANDIDATES\n")

keywords = [
    "audio",
    "mic",
    "microphone",
    "hydro",
    "sound",
    "pcm",
    "wave",
    "sensor_msgs",
]

for s in strings:

    text = s.lower()

    if any(
        k in text
        for k in keywords
    ):

        print(s)

os.remove(tmp.name)

print("\nMCAP removed.")
