import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    balanced_accuracy_score
)

df = pd.read_csv(
    "audio_features.csv"
)

train = df[
    df["tank_id"] != 4
]

test = df[
    df["tank_id"] == 4
]

X_train = train.drop(
    columns=[
        "file_id",
        "tank_id",
        "label"
    ]
)

y_train = train["label"]

X_test = test.drop(
    columns=[
        "file_id",
        "tank_id",
        "label"
    ]
)

y_test = test["label"]

clf = RandomForestClassifier(
    n_estimators=500,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

clf.fit(
    X_train,
    y_train
)

pred = clf.predict(
    X_test
)

print(
    classification_report(
        y_test,
        pred
    )
)

print(
    "\nBalanced Accuracy:",
    balanced_accuracy_score(
        y_test,
        pred
    )
)
