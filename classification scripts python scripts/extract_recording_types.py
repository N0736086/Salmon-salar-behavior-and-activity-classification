import pandas as pd
import re

df = pd.read_csv(
    "repository_inventory.csv"
)

def recording_type(path):

    p = path.lower()

    if "_audio_" in p:
        return "audio"

    if "_av_" in p:
        return "av"

    if "_both_" in p:
        return "both"

    if ".wav" in p:
        return "wav"

    return "other"

df["recording_type"] = (
    df["full_path"]
    .apply(recording_type)
)

print(
    df["recording_type"]
    .value_counts()
)

df.to_csv(
    "repository_inventory.csv",
    index=False
)
