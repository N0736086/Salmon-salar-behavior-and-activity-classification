#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("labeled_audio.csv")

# remove classes with too few examples
keep = [
    "feeding",
    "maintenance",
    "visual_check",
    "routine_operation",
    "handling",
    "cleaning",
    "normal_activity"
]

events = df[df["label"].isin(keep)]

# sample same number of backgrounds
background = df[df["label"] == "background"]

n = len(events)

background = background.sample(
    min(n, len(background)),
    random_state=42
)

training = pd.concat(
    [events, background],
    ignore_index=True
)

training = training.sample(
    frac=1,
    random_state=42
)

training.to_csv(
    "training_manifest.csv",
    index=False
)

print("\nTraining Manifest")
print("------------------")
print(training["label"].value_counts())
print("\nRows:", len(training))
