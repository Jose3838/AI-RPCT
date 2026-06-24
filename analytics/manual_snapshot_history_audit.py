from pathlib import Path
import pandas as pd

history_dir = Path("warehouse/manual_snapshot_history")

files = sorted(history_dir.glob("*.csv"))

rows = []

for f in files:
    try:
        df = pd.read_csv(f)
        rows.append({
            "snapshot_file": f.name,
            "row_count": len(df),
        })
    except Exception:
        pass

pd.DataFrame(rows).to_csv(
    "data/manual_snapshot_history_audit.csv",
    index=False
)

print("history audit generated")
