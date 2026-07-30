import pandas as pd

xls = pd.ExcelFile(
    "AIAFS_X/001128 - AI-AFS- datasheet - ethogram -  2025 - VE.xlsx"
)

for sheet in xls.sheet_names:

    df = pd.read_excel(
        xls,
        sheet_name=sheet
    )

    mask = (
        df.astype(str)
        .apply(
            lambda s: s.str.contains(
                r'feeding|feed|alimentation|food|expérience',
                case=False,
                na=False
            )
        )
        .any(axis=1)
    )

    hits = df[mask]

    if len(hits):
        print("\nSHEET:", sheet)
        print(hits.head(50))
