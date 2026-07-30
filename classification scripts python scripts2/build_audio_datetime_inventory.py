import pandas as pd
import re

df = pd.read_csv("repository_inventory.csv")

def extract_datetime(path):

    m = re.search(
        r'_(20\d{6})_(\d{6})',
        str(path)
    )

    if not m:
        return pd.NaT

    d = m.group(1)
    t = m.group(2)

    return pd.to_datetime(
        d + t,
        format="%Y%m%d%H%M%S",
        errors="coerce"
    )

df["recording_datetime"] = (
    df["file_name"]
    .apply(extract_datetime)
)

wavs = df[
    df["recording_type"] == "wav"
].copy()

wavs.to_csv(
    "audio_datetime_inventory.csv",
    index=False
)

print("WAVs:", len(wavs))

print(
    wavs["recording_datetime"]
    .notna()
    .sum(),
    "with datetime"
)
