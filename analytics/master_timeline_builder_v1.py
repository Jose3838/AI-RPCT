from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/master_timeline_v1.csv")
REPORT = Path("reports/master_timeline_builder_v1.md")


def quarter(month: int) -> str:
    return f"Q{((month - 1) // 3) + 1}"


def main() -> None:
    rows = []

    for year in range(2006, 2027):
        for month in range(1, 13):
            rows.append(
                {
                    "date": f"{year}-{month:02d}-01",
                    "year": year,
                    "month": month,
                    "quarter": quarter(month),
                    "gpu_generation": "",
                    "provider_generation": "",
                    "market_phase": "",
                    "event_count": 0,
                    "source_count": 0,
                    "timeline_version": "v1",
                    "created_at": datetime.now(UTC).isoformat(),
                }
            )

    df = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Master Timeline Builder v1",
                "",
                f"Rows: {len(df)}",
                f"Start: {df.iloc[0]['date']}",
                f"End: {df.iloc[-1]['date']}",
                "",
                "## CTO Assessment",
                "",
                "This master timeline is the canonical monthly calendar",
                "for all historical AI infrastructure data.",
                "",
                "Future datasets should join against this timeline",
                "instead of creating independent date axes.",
            ]
        ),
        encoding="utf-8",
    )

    print("MASTER TIMELINE BUILDER V1")
    print("==========================")
    print(df.head())
    print()
    print(df.tail())
    print(f"\nRows: {len(df)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
