#!/usr/bin/env python3

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier

# ======================================
# LOAD
# ======================================

df = pd.read_csv(
    "segment_features.csv"
)

# remove unknown tanks

df = df[
    df["tank"] != "unknown"
]

print("Dataset:", df.shape)

# ======================================
# FEATURES
# ======================================

X = df.drop(
    columns=[
        "segment_file",
        "tank",
        "label"
    ],
    errors="ignore"
)

encoder = LabelEncoder()

y = encoder.fit_transform(
    df["label"]
)

tanks = sorted(
    df["tank"].unique()
)

results = []

# ======================================
# LOTO LOOP
# ======================================

for test_tank in tanks:

    print("\n")
    print("=" * 60)
    print("TEST TANK:", test_tank)
    print("=" * 60)

    train_mask = (
        df["tank"] != test_tank
    )

    test_mask = (
        df["tank"] == test_tank
    )

    X_train = X.loc[train_mask]
    X_test = X.loc[test_mask]

    y_train = y[train_mask]
    y_test = y[test_mask]

    print(
        f"Train: {len(X_train)}"
    )

    print(
        f"Test:  {len(X_test)}"
    )

    model = XGBClassifier(
        n_estimators=500,
        max_depth=8,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    pred = model.predict(
        X_test
    )

    acc = accuracy_score(
        y_test,
        pred
    )

    f1 = f1_score(
        y_test,
        pred,
        average="weighted"
    )

    print("\nAccuracy:", acc)
    print("Weighted F1:", f1)

    print("\nClassification Report\n")

    print(
        classification_report(
            y_test,
            pred,
            target_names=encoder.classes_
        )
    )

    print("\nConfusion Matrix\n")

    print(
        confusion_matrix(
            y_test,
            pred
        )
    )

    results.append({
        "test_tank": test_tank,
        "accuracy": acc,
        "weighted_f1": f1
    })

# ======================================
# RESULTS
# ======================================

results = pd.DataFrame(
    results
)

results.to_csv(
    "segment_loto_results.csv",
    index=False
)

print("\n")
print("=" * 60)
print("AVERAGE")
print("=" * 60)

print(
    results.mean(
        numeric_only=True
    )
)

print("\nSaved:")
print("segment_loto_results.csv")
