#!/usr/bin/env python3

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report
)

from xgboost import XGBClassifier

# ====================================================
# LOAD DATA
# ====================================================

df = pd.read_csv(
    "acoustic_features_fixed.csv"
)

# remove unknown tank files

df = df[
    df["tank"] != "unknown"
]

print("Dataset shape:", df.shape)

# ====================================================
# FEATURES
# ====================================================

X = df.drop(
    columns=[
        "file_id",
        "label",
        "tank"
    ],
    errors="ignore"
)

# ====================================================
# LABEL ENCODING
# ====================================================

encoder = LabelEncoder()

y = encoder.fit_transform(
    df["label"]
)

# ====================================================
# TANKS
# ====================================================

tanks = sorted(
    df["tank"].unique()
)

results = []

# ====================================================
# LOTO
# ====================================================

for test_tank in tanks:

    print()
    print("=" * 70)
    print("Testing:", test_tank)
    print("=" * 70)

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

    print(
        f"Accuracy: {acc:.4f}"
    )

    print(
        f"Weighted F1: {f1:.4f}"
    )

    print(
        classification_report(
            y_test,
            pred,
            target_names=encoder.classes_,
            zero_division=0
        )
    )

    results.append(
        {
            "test_tank": test_tank,
            "accuracy": acc,
            "weighted_f1": f1
        }
    )

# ====================================================
# SAVE RESULTS
# ====================================================

results = pd.DataFrame(
    results
)

results.to_csv(
    "loto_xgboost_results.csv",
    index=False
)

print()
print("=" * 70)
print("AVERAGE RESULTS")
print("=" * 70)

print(
    results.mean(
        numeric_only=True
    )
)
