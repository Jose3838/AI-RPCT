from pathlib import Path
import pandas as pd

snapshot_files = len(list(Path("warehouse").rglob("*.csv")))
report_files = len(list(Path("reports").glob("*"))) if Path("reports").exists() else 0

data_rows = 0
csv_files = 0

for file in Path("data").glob("*.csv"):
    try:
        df = pd.read_csv(file)
        data_rows += len(df)
        csv_files += 1
    except:
        pass

out = pd.DataFrame([{
    "snapshot_files": snapshot_files,
    "report_files": report_files,
    "data_csv_files": csv_files,
    "total_data_rows": data_rows
}])

out.to_csv("data/history_summary.csv", index=False)

print(out)
