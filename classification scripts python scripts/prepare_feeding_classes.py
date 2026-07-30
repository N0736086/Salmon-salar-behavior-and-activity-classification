import pandas as pd

features = pd.read_csv(
    "audio_features.csv",
    dtype={"file_id": str}
)

audio = pd.read_csv(
    "audio_box_files.csv",
    dtype={"file_id": str}
)

audio["recording_datetime"] = pd.to_datetime(
    audio["recording_datetime"]
)

# ----------------------------------------------------
# MANUAL FEEDING WINDOWS
# ----------------------------------------------------
#
# EDIT THESE DATES/TIMES
#
# class 1 = pre-feed
# class 2 = feeding
# class 3 = post-feed
#
# ----------------------------------------------------

feeding_windows = [

    {
        "tank_id": 1,
        "feeding_start": "2026-05-13 10:00:00",
        "feeding_end":   "2026-05-13 10:15:00"
    },

]

labels = []

for _, row in audio.iterrows():

    label = None

    ts = row["recording_datetime"]

    tank = row["tank_id"]

    for fw in feeding_windows:

        if tank != fw["tank_id"]:
            continue

        feed_start = pd.Timestamp(
            fw["feeding_start"]
        )

        feed_end = pd.Timestamp(
            fw["feeding_end"]
        )

        # 30 min before feed
        pre_start = (
            feed_start -
            pd.Timedelta(minutes=30)
        )

        # 30 min after feed
        post_end = (
            feed_end +
            pd.Timedelta(minutes=30)
        )

        if pre_start <= ts < feed_start:

            label = 1

        elif feed_start <= ts <= feed_end:

            label = 2

        elif feed_end < ts <= post_end:

            label = 3

    if label is not None:

        labels.append({
            "file_id": row["file_id"],
            "feeding_class": label
        })

labels = pd.DataFrame(labels)

dataset = features.merge(
    labels,
    on="file_id",
    how="inner"
)

dataset.to_csv(
    "feeding_classification_dataset.csv",
    index=False
)

print(dataset.shape)

print(
    dataset["feeding_class"]
    .value_counts()
)
