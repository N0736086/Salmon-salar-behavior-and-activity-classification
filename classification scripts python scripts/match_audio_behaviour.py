import pandas as pd

audio = pd.read_csv(
    "audio_on_observation_days.csv"
)

events = pd.read_csv(
    "labelled_behaviour_events.csv"
)

audio["recording_datetime"] = pd.to_datetime(
    audio["recording_datetime"],
    errors="coerce"
)

events["start_datetime"] = pd.to_datetime(
    events["start_datetime"],
    errors="coerce"
)

events["end_datetime"] = pd.to_datetime(
    events["end_datetime"],
    errors="coerce"
)

matches = []

for _, event in events.iterrows():

    tank = str(int(event["tank_id"]))

    candidates = audio[
        audio["tank_id"].astype(str) == tank
    ]

    overlap = candidates[
        (candidates["recording_datetime"] >= event["start_datetime"]) &
        (candidates["recording_datetime"] <= event["end_datetime"])
    ]

    for _, a in overlap.iterrows():

        matches.append({
            "file_name": a["file_name"],
            "full_path": a["full_path"],
            "tank_id": tank,
            "recording_datetime": a["recording_datetime"],
            "behaviour_code": event["behaviour_code"],
            "behaviour_label": event["behaviour_label"]
        })

matched = pd.DataFrame(matches)

matched.to_csv(
    "audio_behaviour_matches.csv",
    index=False
)

print("\nMatches")
print(len(matched))

if len(matched):
    print("\nBehaviour counts")
    print(
        matched["behaviour_code"]
        .value_counts()
    )
