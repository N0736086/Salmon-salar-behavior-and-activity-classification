import pandas as pd

audio = pd.read_csv(
    "master_annotations.csv"
)

eth = pd.read_csv(
    "ethogram_clean.csv"
)

audio["timestamp"] = pd.to_datetime(
    audio["timestamp"],
    errors="coerce"
)

eth["Date"] = pd.to_datetime(
    eth["Date"],
    dayfirst=True,
    errors="coerce"
)

print("Audio date range")
print(audio["timestamp"].min())
print(audio["timestamp"].max())

print("\nEthogram date range")
print(eth["Date"].min())
print(eth["Date"].max())

print("\nUnique labels")
print(
    eth["label"]
    .dropna()
    .value_counts()
)
