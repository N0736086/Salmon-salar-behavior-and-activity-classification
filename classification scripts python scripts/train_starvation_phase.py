import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import (
    classification_report,
    balanced_accuracy_score
)

df = pd.read_csv(
    "starvation_phase_dataset.csv"
)

X = df.drop(
    columns=[
        "file_id",
        "tank_id",
        "label",
        "starvation_phase"
    ],
    errors="ignore"
)

y = df["starvation_phase"]

groups = df["tank_id"]

gkf = GroupKFold(
    n_splits=4
)

scores = []

for fold, (train_idx, test_idx) in enumerate(
    gkf.split(X, y, groups)
):

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    model = RandomForestClassifier(
        n_estimators=500,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    pred = model.predict(
        X_test
    )

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

print(
    "\nMean Balanced Accuracy:"
)

print(
    sum(scores)/len(scores)
)
