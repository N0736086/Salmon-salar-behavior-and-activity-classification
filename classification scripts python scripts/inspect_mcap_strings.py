import tempfile
import requests
import pandas as pd
import re

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

with open(tmp.name, "rb") as f:
    data = f.read()

strings = re.findall(
    rb"[\x20-\x7E]{5,}",
    data
)

keywords = [
    "topic",
    "sensor_msgs",
    "audio",
    "video",
    "image",
    "camera",
    "mic",
    "hydro",
    "compressed"
]

print("\nMATCHES:\n")

for s in strings:

    text = s.decode(
        "utf-8",
        errors="ignore"
    )

    lower = text.lower()

    if any(
        k in lower
        for k in keywords
    ):
        print(text)
