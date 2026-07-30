import pandas as pd

df = pd.read_csv("audio_box_files.csv")

df["recording_datetime"] = pd.to_datetime(
    df["recording_datetime"]
)

df["date"] = df["recording_datetime"].dt.date

for tank in sorted(df["tank_id"].unique()):

    print("\n===================")
    print("TANK", tank)
    print("===================")

    dates = (
        df[df["tank_id"] == tank]["date"]
        .drop_duplicates()
        .sort_values()
    )

    for d in dates:
        print(d)
