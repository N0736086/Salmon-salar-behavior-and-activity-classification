import pandas as pd
import re

df = pd.read_csv("audio_inventory.csv")

def parse_timestamp(name):

    name = str(name)

    patterns = [

        r'(\d{8})_(\d{6})',

        r'(\d{4}-\d{2}-\d{2})_(\d{6})',

    ]

    for p in patterns:

        m = re.search(p, name)

        if m:

            try:

                date_part = m.group(1).replace("-", "")
                time_part = m.group(2)

                return pd.to_datetime(
                    date_part + time_part,
                    format="%Y%m%d%H%M%S"
                )

            except:
                pass

    return pd.NaT

df["recording_start"] = df["name"].apply(parse_timestamp)

df = df[df["recording_start"].notna()]

df.to_csv(
    "recording_times.csv",
    index=False
)

print(df.shape)

print(
    df[
        ["name", "recording_start"]
    ].head(20)
)
