import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "segment_features.csv"
)

print(df["label"].value_counts())

# =====================================
# FEATURES
# =====================================

X = df.drop(
    columns=[
        "segment_file",
        "tank",
        "label"
    ],
    errors="ignore"
)

enc = LabelEncoder()

y = enc.fit_transform(
    df["label"]
)

# =====================================
# SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# =====================================
# MODEL
# =====================================

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

print("\nAccuracy:")
print(
    accuracy_score(
        y_test,
        pred
    )
)

print("\nWeighted F1:")
print(
    f1_score(
        y_test,
        pred,
        average="weighted"
    )
)

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        pred,
        target_names=enc.classes_
    )
)

print("\nConfusion Matrix\n")

print(
    confusion_matrix(
        y_test,
        pred
    )
)
