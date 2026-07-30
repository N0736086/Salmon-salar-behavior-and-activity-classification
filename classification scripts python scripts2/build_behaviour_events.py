import pandas as pd

xlsx = "/home/feliciano/001128_AIAFS_datasheet_ethogram_2025_VE.xlsx"

df = pd.read_excel(
    xlsx,
    sheet_name="Poissons"
)

events = df.rename(
    columns={
        "Poissons": "date",
        "Unnamed: 1": "start_time",
        "Unnamed: 2": "end_time",
        "Unnamed: 3": "duration",
        "Unnamed: 4": "basin",
        "Unnamed: 5": "behaviour_code",
        "Unnamed: 6": "behaviour_label",
        "Unnamed: 7": "behaviour_description",
        "Unnamed: 8": "comments"
    }
)

events["tank_id"] = (
    events["basin"]
    .astype(str)
    .str.extract(r'B-(\d)')
)

events = events[
    events["behaviour_code"]
    .notna()
]

events.to_csv(
    "behaviour_events.csv",
    index=False
)

print(events.shape)
print(events["behaviour_code"].value_counts())
