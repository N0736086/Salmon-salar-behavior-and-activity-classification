import pandas as pd

proto = pd.read_csv("protocol_recordings.csv")
seg = pd.read_csv("segment_manifest.csv")

proto["recording_key"] = (
    proto["name"]
    .str.replace(".wav","",regex=False)
)

matches = []

for _, p in proto.iterrows():

    key = str(p["recording_key"])

    tmp = seg[
        seg.astype(str)
        .apply(
            lambda c: c.str.contains(
                key,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]

    if len(tmp) == 0:
        continue

    tmp = tmp.copy()

    tmp["protocol_label"] = p["protocol_label"]

    matches.append(tmp)

if matches:

    out = pd.concat(matches)

else:

    out = pd.DataFrame()

out.to_csv(
    "protocol_segment_manifest.csv",
    index=False
)

print(out.shape)

if len(out):
    print(out["protocol_label"].value_counts())
