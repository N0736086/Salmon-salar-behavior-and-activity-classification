import os
import re
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

print("MCAP FILES:", len(mcap))

audio_keywords = [
    "audio",
    "mic",
    "microphone",
    "hydro",
    "sound",
    "pcm",
    "wave",
    "audio_common",
    "audiodata"
]

results = []

for idx, row in mcap.iterrows():

    file_id = str(row["file_id"])

    try:

        url = f"https://api.box.com/2.0/files/{file_id}/content"

        r = requests.get(
            url,
            headers=HEADERS,
            stream=True,
            allow_redirects=True,
            timeout=300
        )

        if r.status_code != 200:
            continue

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
            rb"[ -~]{5,}",
            data
        )

        found = []

        for s in strings:

            text = s.decode(
                "utf-8",
                errors="ignore"
            )

            lower = text.lower()

            for kw in audio_keywords:

                if kw in lower:
                    found.append(text)

        if found:

            print(
                "\nAUDIO CANDIDATE:",
                row["file_name"]
            )

            results.append({
                "file_id": file_id,
                "file_name": row["file_name"],
                "matches": " | ".join(
                    sorted(set(found))
                )
            })

        os.remove(tmp.name)

    except Exception as e:

        print(
            "FAILED:",
            row["file_name"]
        )

        print(e)

pd.DataFrame(results).to_csv(
    "audio_mcap_candidates.csv",
    index=False
)

print("\nDONE")
print("CANDIDATES:", len(results))
