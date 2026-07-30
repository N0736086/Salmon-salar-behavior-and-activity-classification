import pandas as pd

df = pd.read_csv("box_inventory.csv")

audio = df[
    df["name"].str.contains(
        r"\.(wav|flac|mp3)$",
        case=False,
        na=False,
        regex=True
    )
]

print(audio.head(20))

print("Audio files:", len(audio))

audio.to_csv(
    "audio_inventory.csv",
    index=False
)
