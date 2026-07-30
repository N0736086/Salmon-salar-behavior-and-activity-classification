import pandas as pd

audio = pd.read_csv("audio_on_observation_days.csv")

audio["recording_datetime"] = pd.to_datetime(
    audio["recording_datetime"],
    errors="coerce"
)

day = "2026-04-23"

d = audio[
    audio["recording_datetime"]
    .dt.strftime("%Y-%m-%d")
    == day
]

print(d[
    ["recording_datetime","tank_id","file_name"]
].sort_values("recording_datetime").head(100))
