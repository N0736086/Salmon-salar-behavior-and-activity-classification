import pandas as pd

df = pd.read_csv("fish_events.csv")

# Remove repeated headers

df = df[
    ~df["Date"].astype(str).str.contains(
        "Date",
        na=False
    )
]

df = df[
    ~df["Code"].astype(str).str.contains(
        "Code",
        na=False
    )
]

df = df[
    ~df["Behavior / Activity"].astype(str).str.contains(
        "Behavior",
        na=False
    )
]

df.to_csv(
    "fish_events_clean.csv",
    index=False
)

print(df.shape)

print(
    df["Code"]
    .value_counts(dropna=False)
    .head(20)
)
