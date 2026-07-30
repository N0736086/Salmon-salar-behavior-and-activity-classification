import pandas as pd

audio = pd.read_csv(
    "audio_on_observation_days.csv"
)

events = pd.read_csv(
    "labelled_behaviour_events.csv"
)

audio["recording_datetime"] = pd.to_datetime(
    audio["recording_datetime"]
)

events["start_datetime"] = pd.to_datetime(
    events["start_datetime"]
)

matches = []

for _, e in events.iterrows():

    tank = e["tank_id"]

    candidates = audio[
        audio["tank_id"] == tank
    ].copy()

    candidates["delta"] = (
        candidates["recording_datetime"]
        - e["start_datetime"]
    ).abs()

    candidates = candidates[
        candidates["delta"]
        <= pd.Timedelta(minutes=60)
    ]

    for _, a in candidates.iterrows():

        matches.append({
            "file_name": a["file_name"],
            "tank_id": tank,
            "behaviour_code": e["behaviour_code"],
            "event_time": e["start_datetime"],
            "audio_time": a["recording_datetime"]
        })

pd.DataFrame(matches).to_csv(
    "audio_behaviour_nearest.csv",
    index=False
)

print(len(matches))
