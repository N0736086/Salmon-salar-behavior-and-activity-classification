import pandas as pd

df = pd.read_csv(
    "labelled_behaviour_events.csv"
)

print(
    df[
        ["tank_id",
         "behaviour_code",
         "start_datetime",
         "end_datetime"]
    ]
    .sort_values("start_datetime")
    .head(100)
)
