import pandas as pd

xlsx = "/home/feliciano/001128_AIAFS_datasheet_ethogram_2025_VE.xlsx"

df = pd.read_excel(
    xlsx,
    sheet_name="Poissons"
)

feeding = df[
    df.astype(str)
      .apply(
          lambda s:
          s.str.contains(
              "aliment",
              case=False,
              na=False
          )
      )
      .any(axis=1)
]

feeding.to_csv(
    "feeding_events.csv",
    index=False
)

print(feeding.shape)

print(
    feeding[
        [
            "Poissons",
            "Unnamed: 1",
            "Unnamed: 2",
            "Unnamed: 4",
            "Unnamed: 8"
        ]
    ]
)
