from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

PROVENANCE_PATH = Path("warehouse/historical/metadata/provenance_log.csv")


def append_provenance(source: str, category: str, output_file: str, row_count: int, trust_grade: str) -> None:
    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "timestamp": datetime.now(UTC).isoformat(),
        "source": source,
        "category": category,
        "output_file": output_file,
        "row_count": row_count,
        "trust_grade": trust_grade,
    }

    if PROVENANCE_PATH.exists():
        df = pd.read_csv(PROVENANCE_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(PROVENANCE_PATH, index=False)
