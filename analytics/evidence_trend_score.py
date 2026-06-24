from pathlib import Path
import pandas as pd

history_dir = Path("warehouse/manual_snapshot_history")

rows = []

for file in sorted(history_dir.glob("*.csv")):
    try:
        df = pd.read_csv(file)

        rows.append({
            "snapshot_date": file.stem.replace("manual_snapshot_", ""),
            "snapshot_count": len(df)
        })
    except Exception:
        pass

trend = pd.DataFrame(rows)

if len(trend) > 1:
    trend["growth"] = trend["snapshot_count"].diff().fillna(0)
else:
    trend["growth"] = 0

trend.to_csv(
    "data/evidence_trend_score.csv",
    index=False
)

print(trend)
