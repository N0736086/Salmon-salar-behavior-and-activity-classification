import pandas as pd

df = pd.read_csv(
    "audio_labelled_dataset.csv"
)

print(df.shape)

print(
    df["tank_id"]
    .value_counts()
)

print(
    df["binary_label"]
    .value_counts()
)
