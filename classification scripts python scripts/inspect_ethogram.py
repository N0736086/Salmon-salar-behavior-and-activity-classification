import pandas as pd

file = "/home/feliciano/Downloads/001128 - AI-AFS- datasheet - ethogram -  2025 - VE.xlsx"

xls = pd.ExcelFile(file)

print("\nSHEETS\n")
for s in xls.sheet_names:
    print(s)

for sheet in xls.sheet_names:

    print("\n" + "=" * 80)
    print("SHEET:", sheet)
    print("=" * 80)

    try:

        df = pd.read_excel(
            file,
            sheet_name=sheet
        )

        print("\nCOLUMNS\n")
        print(df.columns.tolist())

        print("\nHEAD\n")
        print(df.head(10))

    except Exception as e:

        print(e)
