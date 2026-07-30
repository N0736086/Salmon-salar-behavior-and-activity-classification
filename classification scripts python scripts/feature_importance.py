import pandas as pd

from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

df = pd.read_csv(
    "research_features.csv"
)

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

model = XGBClassifier(
    n_estimators=500,
    random_state=42,
    eval_metric="logloss"
)

model.fit(X, y)

importance = pd.DataFrame({

    "feature": X.columns,

    "importance":
    model.feature_importances_

})

importance = (
    importance
    .sort_values(
        "importance",
        ascending=False
    )
)

importance.to_csv(
    "feature_importance.csv",
    index=False
)

print(
    importance.head(20)
)

