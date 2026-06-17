from pathlib import Path
import pandas as pd

snapshots = len(list(Path("warehouse").rglob("*.csv")))
reports = len(list(Path("reports").glob("*")))

rows = 0

for file in Path("data").glob("*.csv"):
    try:
        rows += len(pd.read_csv(file))
    except:
        pass

out = pd.DataFrame([{
    "snapshot_files": snapshots,
    "report_files": reports,
    "tracked_rows": rows
}])

out.to_csv("data/warehouse_metrics.csv", index=False)

print(out)
