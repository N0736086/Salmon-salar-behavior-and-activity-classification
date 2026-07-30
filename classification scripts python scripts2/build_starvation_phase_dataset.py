import pandas as pd

# --------------------------------------------------
# Load audio metadata
# --------------------------------------------------

audio = pd.read_csv(
    "audio_box_files.csv",
    dtype={"file_id": str}
)

audio["recording_datetime"] = pd.to_datetime(
    audio["recording_datetime"]
)

audio["date"] = (
    audio["recording_datetime"]
    .dt.strftime("%Y-%m-%d")
)

# --------------------------------------------------
# Phase labelling
# --------------------------------------------------

def get_phase(tank, date):

    # Tank 1 = Control
    if tank == 1:
        return 0

    # 48 h block
    if date in [
        "2026-04-23",
        "2026-04-24",
        "2026-04-26"
    ]:
        return 1

    # 96 h block
    if date in [
        "2026-05-01",
        "2026-05-09"
    ]:
        return 2

    # 168 h block
    if date in [
        "2026-05-13",
        "2026-05-16",
        "2026-05-21"
    ]:
        return 3

    return None

audio["starvation_phase"] = audio.apply(
    lambda r: get_phase(
        int(r["tank_id"]),
        r["date"]
    ),
    axis=1
)

audio = audio[
    audio["starvation_phase"]
    .notna()
].copy()

audio["starvation_phase"] = (
    audio["starvation_phase"]
    .astype(int)
)

# --------------------------------------------------
# Load features
# --------------------------------------------------

features = pd.read_csv(
    "audio_features.csv",
    dtype={"file_id": str}
)

# --------------------------------------------------
# Merge
# --------------------------------------------------

dataset = features.merge(
    audio[
        [
            "file_id",
            "starvation_phase"
        ]
    ],
    on="file_id",
    how="inner"
)

dataset.to_csv(
    "starvation_phase_dataset.csv",
    index=False
)

print()

print("Dataset shape:")
print(dataset.shape)

print()

print(
    dataset["starvation_phase"]
    .value_counts()
    .sort_index()
)
