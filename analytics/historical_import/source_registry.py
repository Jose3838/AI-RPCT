from __future__ import annotations

from pathlib import Path

import pandas as pd

SOURCE_REGISTRY = Path("data/historical_sources.csv")


def load_sources() -> pd.DataFrame:
    if not SOURCE_REGISTRY.exists():
        return pd.DataFrame()
    return pd.read_csv(SOURCE_REGISTRY)


def source_exists(source: str) -> bool:
    df = load_sources()
    if df.empty or "source" not in df.columns:
        return False
    return source in set(df["source"].astype(str))
