import pandas as pd

df = pd.read_csv("training_manifest_fixed.csv")

stress = df[
    df["label"].isin([
        "maintenance",
        "cleaning",
        "handling",
        "routine_operation"
    ])
]

stress["protocol_label"] = "stress"

stress.to_csv(
    "stress_manifest.csv",
    index=False
)

print(stress.shape)
print(stress["label"].value_counts())
