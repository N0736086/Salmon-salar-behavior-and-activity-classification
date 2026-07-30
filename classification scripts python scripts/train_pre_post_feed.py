import pandas as pd

from sklearn.model_selection import GroupKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    balanced_accuracy_score
)

df = pd.read_csv("audio_features.csv")

df = df.dropna(
    subset=["feeding_state"]
)

X = df.drop(
    columns=[
        "file_id",
        "tank_id",
        "label",
        "feeding_state"
    ],
    errors="ignore"
)

y = df["feeding_state"]

groups = df["tank_id"]

gkf = GroupKFold(n_splits=4)

scores = []

for fold, (train_idx, test_idx) in enumerate(
    gkf.split(X, y, groups)
):

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    clf = RandomForestClassifier(
        n_estimators=500,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    clf.fit(X_train, y_train)

    pred = clf.predict(X_test)

    score = balanced_accuracy_score(
        y_test,
        pred
    )

    scores.append(score)

    print("\nFold", fold + 1)

    print(
        classification_report(
            y_test,
            pred
        )
    )

print("\nAverage Balanced Accuracy")

print(sum(scores)/len(scores))
