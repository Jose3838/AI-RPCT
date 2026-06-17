from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

DATA = Path("data")
DATA.mkdir(exist_ok=True)

NOW = datetime.now(timezone.utc).isoformat()

def append_snapshot(source_file, target_file, rename_map=None):
    source = DATA / source_file
    target = DATA / target_file

    if not source.exists():
        print(f"missing: {source}")
        return

    df = pd.read_csv(source)
    df.insert(0, "timestamp", NOW)

    if rename_map:
        df = df.rename(columns=rename_map)

    if target.exists():
        old = pd.read_csv(target)
        df = pd.concat([old, df], ignore_index=True)

    df.to_csv(target, index=False)
    print(f"snapshot appended: {target} rows={len(df)}")

append_snapshot(
    "live_gpu_price_index.csv",
    "gpu_price_history.csv"
)

append_snapshot(
    "provider_health.csv",
    "provider_health_history.csv"
)

append_snapshot(
    "live_provider_market_share.csv",
    "provider_market_share_history.csv"
)

print("history snapshot complete")
