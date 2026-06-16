from pathlib import Path
from shutil import copy2
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

snapshot_dir = Path("warehouse/snapshots")
snapshot_dir.mkdir(parents=True, exist_ok=True)

files = [
    "data/provider_rankings.csv",
    "data/provider_marketshare.csv",
    "data/provider_concentration.csv",
    "data/rpct_scores.csv",
    "data/forecast_signal.csv",
    "data/alerts.csv"
]

for file in files:
    path = Path(file)

    if path.exists():
        target = snapshot_dir / f"{today}_{path.name}"
        copy2(path, target)
        print(f"Archived: {target}")

print("Daily snapshot archive complete.")
