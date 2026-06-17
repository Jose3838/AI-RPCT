from pathlib import Path
from shutil import copy2
from datetime import datetime

source = Path("data/live_provider_data.csv")

if source.exists():
    Path("warehouse/live_provider_history").mkdir(
        parents=True,
        exist_ok=True
    )

    target = Path(
        f"warehouse/live_provider_history/{datetime.now().strftime('%Y-%m-%d')}_vast.csv"
    )

    copy2(source, target)

    print(f"Archived: {target}")
else:
    print("No live provider data found.")
