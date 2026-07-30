import pandas as pd

df = pd.read_csv("training_manifest_fixed.csv")

def protocol_label(x):

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
    .apply(protocol_label)
)

df.to_csv(
    "protocol_manifest.csv",
    index=False
)

print(
    df["protocol_label"]
    .value_counts()
)
