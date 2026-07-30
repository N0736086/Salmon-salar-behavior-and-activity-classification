import pandas as pd

df = pd.read_csv("box_file_map.csv", dtype={"file_id": str})

bg = df[
    df["path"].str.contains(
        "without fish",
        case=False,
        na=False
    )
].copy()

bg = bg[
    bg["file_name"]
    .str.lower()
    .str.endswith(".wav", na=False)
]

bg["class"] = 0

bg[["file_id", "class", "file_name", "path"]].to_csv(
    "background_labels.csv",
    index=False
)

print("Background WAVs:", len(bg))
