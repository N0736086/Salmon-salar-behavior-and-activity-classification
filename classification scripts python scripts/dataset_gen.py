import pandas as pd

df = pd.read_csv(
    "labelled_behaviour_events.csv"
)

df = df[
    df["behaviour_code"].isin(
        ["P1","P2","P3","P4"]
    )
].copy()

df["binary_label"] = (
    df["behaviour_code"]
    .apply(
        lambda x:
        "healthy"
        if x=="P1"
        else "abnormal"
    )
)

df.to_csv(
    "final_behaviour_labels.csv",
    index=False
)

print(df["binary_label"].value_counts())
