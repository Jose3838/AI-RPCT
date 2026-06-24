from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
WAREHOUSE_DIR = Path("warehouse/provider_timeseries")

INPUTS = [
    DATA_DIR / "vast_live_report.csv",
    DATA_DIR / "runpod_live_report.csv",
]


def normalize_rows(df: pd.DataFrame, source_file: Path) -> pd.DataFrame:
    provider = source_file.stem.replace("_live_report", "")
    now = datetime.now(UTC).isoformat()

    rows = []

    for _, row in df.iterrows():
        rows.append(
            {
                "timestamp": row.get("timestamp", now),
                "provider": row.get("provider", provider),
                "gpu": row.get("gpu", row.get("gpu_type", "unknown")),
                "price_per_hour": row.get("price_per_hour", 0),
                "availability": row.get("availability", row.get("available_capacity", 0)),
                "source_file": str(source_file),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    written = []

    for path in INPUTS:
        if not path.exists() or path.stat().st_size <= 1:
            continue

        df = pd.read_csv(path)
        if df.empty:
            continue

        normalized = normalize_rows(df, path)
        provider = path.stem.replace("_live_report", "")
        date_key = datetime.now(UTC).date().isoformat()
        out = WAREHOUSE_DIR / f"{date_key}_{provider}.csv"

        if out.exists():
            existing = pd.read_csv(out)
            normalized = pd.concat([existing, normalized], ignore_index=True)

        normalized.to_csv(out, index=False)
        written.append(str(out))

    print("PROVIDER HISTORY WRITER")
    print("=======================")
    print(f"Files written: {len(written)}")
    for item in written:
        print(item)


if __name__ == "__main__":
    main()
