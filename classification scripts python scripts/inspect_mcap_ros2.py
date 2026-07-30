import os
import tempfile
import requests
import pandas as pd

from mcap_ros2.reader import read_ros2_messages

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
    tmp.write(chunk)

tmp.close()

topics = set()

try:

    for msg in read_ros2_messages(tmp.name):

        topics.add(msg.channel.topic)

        if len(topics) > 50:
            break

except Exception as e:

    print("ERROR:")
    print(e)

print("\nTOPICS FOUND\n")

for t in sorted(topics):
    print(t)

os.remove(tmp.name)
