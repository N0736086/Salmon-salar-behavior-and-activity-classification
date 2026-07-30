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

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "segment_features_protocol.csv"
)

# Remove unknown tanks

df = df[
    df["tank"] != "unknown"
]

print("\nDataset shape:", df.shape)

print("\nClass distribution:")
print(
    df["protocol_label"]
    .value_counts()
)

# =====================================================
# FEATURES
# =====================================================

X = df.drop(
    columns=[
        "segment_file",
        "label",
        "protocol_label",
        "tank"
    ],
    errors="ignore"
)

# =====================================================
# LABELS
# =====================================================

encoder = LabelEncoder()

y = encoder.fit_transform(
    df["protocol_label"]
)

print("\nClasses:")
print(
    list(
        encoder.classes_
    )
)

# =====================================================
# LEAVE ONE TANK OUT
# =====================================================

tanks = sorted(
    df["tank"].unique()
)

results = []

for test_tank in tanks:

    print("\n")
    print("=" * 70)
    print(f"TEST TANK: {test_tank}")
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

    print(
        f"Train samples: {len(X_train)}"
    )

    print(
        f"Test samples: {len(X_test)}"
    )

    model = XGBClassifier(
        n_estimators=500,
        max_depth=8,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="mlogloss"
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

    weighted_f1 = f1_score(
        y_test,
        pred,
        average="weighted"
    )

    macro_f1 = f1_score(
        y_test,
        pred,
        average="macro"
    )

    print(
        f"\nAccuracy: {acc:.4f}"
    )

    print(
        f"Weighted F1: {weighted_f1:.4f}"
    )

    print(
        f"Macro F1: {macro_f1:.4f}"
    )

    print("\nClassification Report\n")

    print(
        classification_report(
            y_test,
            pred,
            target_names=encoder.classes_,
            zero_division=0
        )
    )

    cm = confusion_matrix(
        y_test,
        pred
    )

    print("\nConfusion Matrix\n")

    print(cm)

    results.append({
        "tank": test_tank,
        "accuracy": acc,
        "weighted_f1": weighted_f1,
        "macro_f1": macro_f1
    })

# =====================================================
# SAVE RESULTS
# =====================================================

results = pd.DataFrame(
    results
)

results.to_csv(
    "protocol_segment_loto_results.csv",
    index=False
)

print("\n")
print("=" * 70)
print("AVERAGE RESULTS")
print("=" * 70)

print(
    results.mean(
        numeric_only=True
    )
)

print(
    "\nSaved: protocol_segment_loto_results.csv"
)
