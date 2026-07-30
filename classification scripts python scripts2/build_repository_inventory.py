import pandas as pd
import re

tree_file = "box_tree.txt"

rows = []

with open(tree_file, "r", encoding="utf-8", errors="ignore") as f:

    for line in f:

        line = line.strip()

        if not line.startswith("[FILE]"):
            continue

        path = line.replace("[FILE]", "").strip()

        filename = path.split("/")[-1]

        tank = None

        patterns = [
            r"tank([1-4])",
            r"Tank_([1-4])",
            r"/Tank_([1-4])/",
            r"/Comp[A-Z]_tank([1-4])/"
        ]

        for p in patterns:

            m = re.search(p, path, flags=re.I)

            if m:
                tank = m.group(1)
                break

        rows.append({
            "full_path": path,
            "file_name": filename,
            "tank_id": tank
        })

df = pd.DataFrame(rows)

df.to_csv(
    "repository_inventory.csv",
    index=False
)

print(df.shape)

print("\nTank counts")

print(
    df["tank_id"]
    .value_counts(dropna=False)
)
