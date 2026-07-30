import pandas as pd

from scipy.stats import mannwhitneyu

df = pd.read_csv(
    "d42_features.csv"
)

feeding = (
    df[df.protocol_label=="feeding"]
)

baseline = (
    df[df.protocol_label=="baseline"]
)

features = [

    "rms",

    "zcr",

    "spectral_centroid",

    "spectral_bandwidth",

    "mfcc_mean",

    "mfcc_std",

    "spl_proxy",

    "burst_proxy",

    "turbulence_proxy"
]

rows = []

for f in features:

    stat, p = mannwhitneyu(
        feeding[f],
        baseline[f]
    )

    rows.append({

        "feature": f,

        "feeding_mean":
        feeding[f].mean(),

        "baseline_mean":
        baseline[f].mean(),

        "p_value": p
    })

out = pd.DataFrame(rows)

out.to_csv(
    "feature_statistics.csv",
    index=False
)

print(out)

