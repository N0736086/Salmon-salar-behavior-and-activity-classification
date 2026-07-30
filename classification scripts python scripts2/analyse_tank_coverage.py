import pandas as pd

df = pd.read_csv(
    "repository_inventory.csv"
)

print("\nTotal files")
print(len(df))

print("\nTank counts")
print(
    df["tank_id"]
    .value_counts(dropna=False)
)

missing = df[
    df["tank_id"].isna()
]

print("\nFiles without tank")
print(len(missing))

missing.to_csv(
    "missing_tank_assignment.csv",
    index=False
)
