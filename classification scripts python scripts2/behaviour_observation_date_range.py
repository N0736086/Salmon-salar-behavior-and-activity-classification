import pandas as pd

audio = pd.read_csv(
    "audio_datetime_inventory.csv"
)

events = pd.read_csv(
    "labelled_behaviour_events.csv"
)

audio["date"] = pd.to_datetime(
    audio["recording_datetime"]
).dt.date

events["date"] = pd.to_datetime(
    events["start_datetime"]
).dt.date

match_dates = set(events["date"])

overlap = audio[
    audio["date"].isin(match_dates)
]

print("Audio files on observation dates:")
print(len(overlap))

overlap.to_csv(
    "audio_on_observation_days.csv",
    index=False
)
