import pandas as pd

audio = pd.read_csv(
    "audio_box_files.csv"
)

feed = pd.read_csv(
    "feeding_events.csv"
)

audio["recording_datetime"] = pd.to_datetime(
    audio["recording_datetime"]
)

feed["feed_start"] = pd.to_datetime(
    feed["Date"] + " " + feed["Time entered"]
)

feed["feed_end"] = pd.to_datetime(
    feed["Date"] + " " + feed["Exit time"]
)

labels = []

for _, r in feed.iterrows():

    feed_start = r["feed_start"]
    feed_end = r["feed_end"]

    pre_start = (
        feed_start -
        pd.Timedelta(minutes=30)
    )

    post_end = (
        feed_end +
        pd.Timedelta(minutes=30)
    )

    pre = audio[
        (audio["recording_datetime"] >= pre_start)
        &
        (audio["recording_datetime"] < feed_start)
    ]

    feed_files = audio[
        (audio["recording_datetime"] >= feed_start)
        &
        (audio["recording_datetime"] <= feed_end)
    ]

    post = audio[
        (audio["recording_datetime"] > feed_end)
        &
        (audio["recording_datetime"] <= post_end)
    ]

    for fid in pre["file_id"]:
        labels.append(
            (fid,1)
        )

    for fid in feed_files["file_id"]:
        labels.append(
            (fid,2)
        )

    for fid in post["file_id"]:
        labels.append(
            (fid,3)
        )

labels = pd.DataFrame(
    labels,
    columns=[
        "file_id",
        "class"
    ]
)

labels = labels.drop_duplicates()

labels.to_csv(
    "feeding_labels.csv",
    index=False
)

print(
    labels["class"]
    .value_counts()
)
