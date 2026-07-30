import pandas as pd

df = pd.read_csv("segment_features.csv")

def map_class(x):

    if x == "feeding":
        return "feeding"

    if x in [
        "maintenance",
        "handling",
        "cleaning",
        "routine_operation"
    ]:
        return "stress"

    return "baseline"

df["protocol_label"] = (
    df["label"]
    .apply(map_class)
)

df.to_csv(
    "d42_dataset.csv",
    index=False
)

print(
    df["protocol_label"]
    .value_counts()
)
