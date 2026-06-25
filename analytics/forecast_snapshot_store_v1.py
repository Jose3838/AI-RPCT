from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

FORECAST_PATH = Path("data/forecast_engine_v1.csv")
OUT_DIR = Path("warehouse/forecast_snapshots")
INDEX_PATH = Path("data/forecast_snapshot_index.csv")


def main() -> None:
    if not FORECAST_PATH.exists() or FORECAST_PATH.stat().st_size <= 1:
        raise SystemExit("forecast_engine_v1.csv missing or empty")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(UTC)
    snapshot_id = now.strftime("%Y%m%dT%H%M%SZ")
    out_file = OUT_DIR / f"forecast_snapshot_{snapshot_id}.csv"

    df = pd.read_csv(FORECAST_PATH)
    df["snapshot_id"] = snapshot_id
    df["snapshot_timestamp"] = now.isoformat()

    df.to_csv(out_file, index=False)

    index_row = {
        "snapshot_id": snapshot_id,
        "snapshot_timestamp": now.isoformat(),
        "forecast_rows": len(df),
        "output_file": str(out_file),
    }

    if INDEX_PATH.exists():
        index = pd.read_csv(INDEX_PATH)
        index = pd.concat([index, pd.DataFrame([index_row])], ignore_index=True)
    else:
        index = pd.DataFrame([index_row])

    index.to_csv(INDEX_PATH, index=False)

    print("FORECAST SNAPSHOT STORE V1")
    print("==========================")
    print(f"Snapshot ID: {snapshot_id}")
    print(f"Rows       : {len(df)}")
    print(f"CSV        : {out_file}")
    print(f"Index      : {INDEX_PATH}")


if __name__ == "__main__":
    main()
