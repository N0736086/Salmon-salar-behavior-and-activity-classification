# train_baseline.py

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score
)

df = pd.read_csv("audio_features.csv")

X = df.drop(
    columns=[
        "file_id",
        "tank_id",
        "label"
    ]
)

y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

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

pred = model.predict(X_test)

print("\nClassification Report\n")
print(
    classification_report(
        y_test,
        pred
    )
)

print("\nBalanced Accuracy\n")
print(
    balanced_accuracy_score(
        y_test,
        pred
    )
)

print("\nConfusion Matrix\n")
print(
    confusion_matrix(
        y_test,
        pred
    )
)
