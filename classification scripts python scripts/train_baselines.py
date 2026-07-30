#!/usr/bin/env python3

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

df = pd.read_csv("acoustic_features.csv")

X = df.drop(
    columns=["file_id", "label", "tank"],
    errors="ignore"
)

y = df["label"]

encoder = LabelEncoder()
y = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
    "SVM": SVC(),
    "RandomForest": RandomForestClassifier(
        n_estimators=300,
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        random_state=42
    )
}

for name, model in models.items():

    print("\n" + "="*60)
    print(name)
    print("="*60)

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print(
        "Accuracy:",
        accuracy_score(y_test, pred)
    )

    print(
        "Weighted F1:",
        f1_score(
            y_test,
            pred,
            average="weighted"
        )
    )

    print(
        classification_report(
            y_test,
            pred,
            target_names=encoder.classes_
        )
    )

