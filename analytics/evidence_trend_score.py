from pathlib import Path
import pandas as pd

history = Path("warehouse/manual_snapshot_history")

files = sorted(history.glob("*.csv"))

rows = []

for file in files:
    try:
        df = pd.read_csv(file)

        rows.append({
            "snapshot_date": file.stem.replace("manual_snapshot_", ""),
            "snapshot_count": len(df)
        })

    except Exception:
        pass

trend = pd.DataFrame(rows)

if len(trend) >= 2:
    trend["growth"] = trend["snapshot_count"].diff()
else:
    trend["growth"] = 0

trend.to_csv(
    "data/evidence_trend_score.csv",
    index=False
)

print(trend)
