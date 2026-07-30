import pandas as pd

df = pd.read_csv(
    "behaviour_events.csv"
)

print("\nBehaviour counts\n")

print(
    df["behaviour_code"]
    .value_counts()
)

print("\nBehaviour labels\n")

print(
    df[
        ["behaviour_code",
         "behaviour_label"]
    ]
    .drop_duplicates()
    .sort_values("behaviour_code")
)
