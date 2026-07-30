import pandas as pd

audio = pd.read_csv(
    "audio_on_observation_days.csv"
)

events = pd.read_csv(
    "final_behaviour_labels.csv"
)

audio["recording_datetime"] = pd.to_datetime(
    audio["recording_datetime"],
    errors="coerce"
)

audio["date"] = (
    audio["recording_datetime"]
    .dt.date
)

events["start_datetime"] = pd.to_datetime(
    events["start_datetime"]
)

events["date"] = (
    events["start_datetime"]
    .dt.date
)

events["tank_id"] = (
    events["tank_id"]
    .astype(int)
)

audio["tank_id"] = (
    audio["tank_id"]
    .fillna(-1)
    .astype(int)
)

labels = events[
    ["date","tank_id","binary_label"]
].drop_duplicates()

dataset = audio.merge(
    labels,
    on=["date","tank_id"],
    how="inner"
)

dataset.to_csv(
    "audio_labelled_dataset.csv",
    index=False
)

print(dataset.shape)

print(
    dataset["binary_label"]
    .value_counts()
)
