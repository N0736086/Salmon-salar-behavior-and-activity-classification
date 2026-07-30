import pandas as pd

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    f1_score
)

from xgboost import XGBClassifier

df = pd.read_csv(
    "research_features.csv"
)

df = df[
    df["tank"] != "unknown"
]

X = df.drop(
    columns=[
        "segment_file",
        "tank",
        "label",
        "protocol_label"
    ],
    errors="ignore"
)

enc = LabelEncoder()

y = enc.fit_transform(
    df["protocol_label"]
)

results = []

for tank in sorted(
    df["tank"].unique()
):

    train = (
        df["tank"] != tank
    )

    test = (
        df["tank"] == tank
    )

    model = XGBClassifier(
        n_estimators=500,
        max_depth=8,
        learning_rate=0.03,
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(
        X.loc[train],
        y[train]
    )

    pred = model.predict(
        X.loc[test]
    )

    acc = accuracy_score(
        y[test],
        pred
    )

    f1 = f1_score(
        y[test],
        pred,
        average="weighted"
    )

    results.append(
        [tank, acc, f1]
    )

results = pd.DataFrame(
    results,
    columns=[
        "tank",
        "accuracy",
        "weighted_f1"
    ]
)

results.to_csv(
    "research_loto_results.csv",
    index=False
)

print(results)

print(
    "\nAverage:"
)

print(
    results.mean(
        numeric_only=True
    )
)

