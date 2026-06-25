from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT_DIR = Path("warehouse/historical/gpu_releases")
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = OUT_DIR / "gpu_release_history.csv"

GPU_RELEASES = [
    ("2006-06-01", "Tesla", "Tesla C870"),
    ("2008-06-16", "Tesla", "Tesla S1070"),
    ("2010-07-12", "Fermi", "Tesla C2050"),
    ("2012-03-22", "Kepler", "Tesla K20"),
    ("2014-03-25", "Maxwell", "GTX 750 Ti"),
    ("2016-05-27", "Pascal", "P100"),
    ("2017-05-10", "Volta", "V100"),
    ("2018-09-20", "Turing", "RTX 2080 Ti"),
    ("2020-05-14", "Ampere", "A100"),
    ("2022-03-22", "Ampere", "A30"),
    ("2022-09-20", "Ada Lovelace", "RTX 4090"),
    ("2023-03-21", "Hopper", "H100"),
    ("2024-03-18", "Blackwell", "B200"),
    ("2024-06-02", "Blackwell", "GB200"),
]

def main():
    rows = []
    created_at = datetime.now(UTC).isoformat()

    for date, architecture, gpu in GPU_RELEASES:
        rows.append({
            "release_date": date,
            "architecture": architecture,
            "gpu": gpu,
            "vendor": "NVIDIA",
            "source": "Historical Archive",
            "trust_grade": "A",
            "created_at": created_at,
        })

    df = pd.DataFrame(rows)
    df.sort_values("release_date", inplace=True)
    df.to_csv(OUT_FILE, index=False)

    print("HISTORICAL GPU RELEASE IMPORT")
    print("=============================")
    print(f"Rows: {len(df)}")
    print(f"CSV : {OUT_FILE}")

if __name__ == "__main__":
    main()
