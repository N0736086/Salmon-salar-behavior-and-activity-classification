import os
import time
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

DATASET_PATH = "/media/feliciano/Aux/AI_AFS_DATASET/feeding_dataset_2s"

SAMPLE_RATE = 8000
N_MELS = 128

# ---------------------------------------------------------
# FEATURE EXTRACTION
# ---------------------------------------------------------

def extract_features(file_path):

    y, sr = librosa.load(
        file_path,
        sr=SAMPLE_RATE,
        mono=True
    )

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=N_MELS,
        fmax=1000
    )

    mel_db = librosa.power_to_db(
        mel,
        ref=np.max
    )

    contrast = librosa.feature.spectral_contrast(
        y=y,
        sr=sr,
        fmin=50,
        n_bands=6
    )

    features = np.concatenate([
        mel_db.flatten(),
        contrast.flatten()
    ])

    return features

# ---------------------------------------------------------
# LABEL MAPPING
# ---------------------------------------------------------

def map_label_from_path(path):

    p = path.lower()

    if "background" in p:
        return "background"

    if "pre" in p and "feed" in p:
        return "pre-feeding"

    if "post" in p and "feed" in p:
        return "post-feeding"

    if "feeding" in p:
        return "feeding"

    return None

# ---------------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------------

print("Loading dataset...")

X = []
y = []

count = 0

for root, dirs, files in os.walk(DATASET_PATH):

    for file in files:

        if file.lower().endswith(".wav"):

            file_path = os.path.join(root, file)

            label = map_label_from_path(root)

            if label is None:
                continue

            try:

                features = extract_features(file_path)

                X.append(features)
                y.append(label)

                count += 1

                if count % 5000 == 0:
                    print(
                        f"Loaded {count} samples..."
                    )

            except Exception as e:

                print(
                    "FAILED:",
                    file_path,
                    e
                )

X = np.array(X)
y = np.array(y)

print("\nLoaded samples:", X.shape[0])
print("Feature vector length:", X.shape[1])
print("Classes found:", set(y))

# ---------------------------------------------------------
# ENCODING
# ---------------------------------------------------------

print("\nEncoding labels...")

le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ---------------------------------------------------------
# SCALING
# ---------------------------------------------------------

print("Scaling features...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("Scaling complete.")

# ---------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------

print("Creating train/test split...")

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print(
    f"Train samples: {len(X_train)}"
)

print(
    f"Test samples: {len(X_test)}"
)

# ---------------------------------------------------------
# TRAIN LINEAR SVM
# ---------------------------------------------------------

print("\nTraining LinearSVC...")

svm = LinearSVC(
    random_state=42,
    max_iter=10000
)

start_train = time.time()

svm.fit(
    X_train,
    y_train
)

train_time = (
    time.time()
    - start_train
)

print(
    "Training complete."
)

# ---------------------------------------------------------
# INFERENCE
# ---------------------------------------------------------

print("Running inference...")

start_inf = time.time()

y_pred = svm.predict(
    X_test
)

inf_time = (
    time.time()
    - start_inf
) / len(X_test)

# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------

acc = accuracy_score(
    y_test,
    y_pred
)

prec = precision_score(
    y_test,
    y_pred,
    average="macro"
)

rec = recall_score(
    y_test,
    y_pred,
    average="macro"
)

f1 = f1_score(
    y_test,
    y_pred,
    average="macro"
)

cm = confusion_matrix(
    y_test,
    y_pred
)

# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

print("\n----------------------")
print("LINEAR SVM RESULTS")
print("----------------------")

print(
    "Training time:",
    round(train_time, 2),
    "s"
)

print(
    "Inference/sample:",
    round(
        inf_time * 1000,
        6
    ),
    "ms"
)

print(
    "Accuracy:",
    round(acc, 4)
)

print(
    "Precision:",
    round(prec, 4)
)

print(
    "Recall:",
    round(rec, 4)
)

print(
    "F1-score:",
    round(f1, 4)
)

print(
    "\nConfusion Matrix:\n",
    cm
)

# ---------------------------------------------------------
# CONFUSION MATRIX PLOT
# ---------------------------------------------------------

plt.figure(
    figsize=(8, 6)
)

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="viridis",
    xticklabels=le.classes_,
    yticklabels=le.classes_,
    linewidths=0.5,
    linecolor="gray"
)

plt.title(
    "Confusion Matrix - Linear SVM"
)

plt.xlabel(
    "Predicted Label"
)

plt.ylabel(
    "True Label"
)

plt.tight_layout()

plt.show()
