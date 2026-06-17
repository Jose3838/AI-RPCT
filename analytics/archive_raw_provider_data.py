from pathlib import Path
from shutil import copy2
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
target_dir = Path("warehouse/raw_providers")
target_dir.mkdir(parents=True, exist_ok=True)

source = Path("data/gpu_data.csv")

if source.exists():
    target = target_dir / f"{today}_gpu_data.csv"
    copy2(source, target)
    print(f"Archived raw provider data: {target}")
else:
    print("No gpu_data.csv found")
