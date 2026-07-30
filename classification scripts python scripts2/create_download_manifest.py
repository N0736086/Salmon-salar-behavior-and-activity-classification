import pandas as pd

box = pd.read_csv(
    "box_file_map.csv",
    dtype={"file_id": str}
)

feed = pd.read_csv(
    "feeding_labels.csv",
    dtype={"file_id": str}
)

bg = pd.read_csv(
    "background_labels.csv",
    dtype={"file_id": str}
)

labels = pd.concat([
    bg[["file_id","class"]],
    feed[["file_id","class"]]
])

labels = labels.drop_duplicates()

manifest = labels.merge(
    box,
    on="file_id",
    how="left"
)

manifest.to_csv(
    "download_manifest.csv",
    index=False
)

print(manifest["class"].value_counts())
print("Saved download_manifest.csv")
