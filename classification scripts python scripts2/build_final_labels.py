import pandas as pd

feed = pd.read_csv(
    "feeding_labels.csv",
    dtype={"file_id": str}
)

bg = pd.read_csv(
    "background_labels.csv",
    dtype={"file_id": str}
)

final = pd.concat([
    bg[["file_id", "class"]],
    feed[["file_id", "class"]]
])

final = final.drop_duplicates()

final.to_csv(
    "final_4class_labels.csv",
    index=False
)

print(final["class"].value_counts())
