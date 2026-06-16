import pandas as pd
from pathlib import Path
from database.db import get_connection

conn = get_connection()

files = {
    "rpct_scores": "data/rpct_scores.csv",
    "provider_rankings": "data/provider_rankings.csv",
    "forecasts": "data/forecast_signal.csv"
}

for table, path in files.items():
    if Path(path).exists():
        df = pd.read_csv(path)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"Imported {path} -> {table}")

conn.close()
print("CSV import complete.")
