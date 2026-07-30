import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from xgboost import XGBClassifier

df = pd.read_csv(
    "protocol_segment_features.csv"
)

drop_cols = []

for c in df.columns:

    if c == "protocol_label":
        continue

    if df[c].dtype == object:
        drop_cols.append(c)

X = df.drop(
    columns=drop_cols + ["protocol_label"],
    errors="ignore"
)

enc = LabelEncoder()

y = enc.fit_transform(
    df["protocol_label"]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    stratify=y,
    test_size=0.2,
    random_state=42
)

model = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.03,
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

print(
    classification_report(
        y_test,
        pred,
        target_names=enc.classes_
    )
)
