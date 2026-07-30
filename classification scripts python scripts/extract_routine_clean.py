import pandas as pd

file = "AIAFS_X/001128 - AI-AFS- datasheet - ethogram -  2025 - VE.xlsx"

df = pd.read_excel(
    file,
    sheet_name="Routine",
    header=None
)

# Find first occurrence of Date row
header_idx = df[
    df.iloc[:,0].astype(str).str.contains(
        "Date",
        na=False
    )
].index[0]

headers = df.iloc[header_idx].tolist()

data = df.iloc[header_idx+1:].copy()

data.columns = headers

data = data.dropna(
    subset=["Date"]
)

cols = [
    "Date",
    "Time entered",
    "Exit time",
    "Code",
    "Behavior / Activity"
]

data = data[cols]

data.to_csv(
    "routine_events.csv",
    index=False
)

print(data.head())
print(data.shape)
