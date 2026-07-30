import pandas as pd

file = "/home/feliciano/Downloads/001128 - AI-AFS- datasheet - ethogram -  2025 - VE.xlsx"

df = pd.read_excel(
    file,
    sheet_name="Poissons",
    header=1
)

def has_feed(row):

    text = " ".join(
        str(x)
        for x in row
        if pd.notna(x)
    ).lower()

    return "alimentation" in text

feeding = df[
    df.apply(
        has_feed,
        axis=1
    )
].copy()

feeding.to_csv(
    "feeding_events.csv",
    index=False
)

print("Feeding events:", len(feeding))

print(
    feeding[
        [
            "Date",
            "Time entered",
            "Exit time",
            "Description"
        ]
    ].head(20)
)
