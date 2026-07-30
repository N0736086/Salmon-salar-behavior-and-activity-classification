import pandas as pd

df = pd.read_csv(
    "repository_inventory.csv"
)

print("\nFILES PER TANK\n")

print(
    pd.crosstab(
        df["tank_id"],
        df["recording_type"]
    )
)

print("\nDATE RANGE\n")

print(
    df["date_token"]
    .min()
)

print(
    df["date_token"]
    .max()
)

