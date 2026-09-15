# create_group_split.py

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

SEED = 42

df = pd.read_csv(
    "dataset_manifest.csv"
)

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=SEED
)

train_idx, test_idx = next(
    gss.split(
        df,
        groups=df["parent_file_id"]
    )
)

df["split"] = "train"
df.loc[test_idx, "split"] = "test"

group_split = (
    df[
        ["parent_file_id", "split"]
    ]
    .drop_duplicates()
)

group_split.to_csv(
    "group_split.csv",
    index=False
)

print(
    group_split["split"]
    .value_counts()
)
