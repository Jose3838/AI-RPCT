from __future__ import annotations

from pathlib import Path

import pandas as pd

HISTORICAL_PATH = Path("data/historical_master_dataset.csv")
LIVE_DIR = Path("warehouse/provider_timeseries")
OUT_PATH = Path("data/combined_market_intelligence_dataset.csv")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def load_historical() -> pd.DataFrame:
    df = read_csv(HISTORICAL_PATH)
    if df.empty:
        return df

    df["intelligence_layer"] = "historical_archive"
    return df


def load_live_timeseries() -> pd.DataFrame:
    frames = []

    if not LIVE_DIR.exists():
        return pd.DataFrame()

    for path in LIVE_DIR.rglob("*.csv"):
        df = read_csv(path)
        if df.empty:
            continue

        df["dataset"] = "provider_timeseries"
        df["source_file"] = path.name
        df["intelligence_layer"] = "live_provider_timeseries"
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True, sort=False)


def main() -> None:
    historical = load_historical()
    live = load_live_timeseries()

    combined = pd.concat([historical, live], ignore_index=True, sort=False)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUT_PATH, index=False)

    print("COMBINED MARKET INTELLIGENCE DATASET")
    print("====================================")
    print(f"Historical rows: {len(historical)}")
    print(f"Live rows      : {len(live)}")
    print(f"Total rows     : {len(combined)}")
    print(f"CSV            : {OUT_PATH}")


if __name__ == "__main__":
    main()
