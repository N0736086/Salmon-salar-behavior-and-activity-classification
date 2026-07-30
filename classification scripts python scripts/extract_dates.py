import pandas as pd
import re

df = pd.read_csv(
    "repository_inventory.csv"
)

def extract_date(path):

    m = re.search(
        r'(20\d{6})',
        path
    )

    if m:
        return m.group(1)

    return None

df["date_token"] = (
    df["full_path"]
    .apply(extract_date)
)

df.to_csv(
    "repository_inventory.csv",
    index=False
)

print(
    df["date_token"]
    .dropna()
    .head()
)

