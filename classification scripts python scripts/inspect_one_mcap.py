# inspect_one_mcap.py

import os
import tempfile
import requests

from mcap.reader import make_reader

TOKEN = "fxG8qkF57nCIN2yTcFFV7Kr0rJj5Ilrp"

FILE_ID = "PUT_ONE_MCAP_FILE_ID_HERE"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

url = (
    f"https://api.box.com/2.0/files/"
    f"{FILE_ID}/content"
)

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

print("Downloaded:", tmp.name)

topics = set()

with open(tmp.name, "rb") as f:

    reader = make_reader(f)

    for schema, channel, message in reader.iter_messages():

        topics.add(channel.topic)

print("\nTopics Found:\n")

for t in sorted(topics):
    print(t)

os.remove(tmp.name)

print("\nTemporary MCAP removed.")
