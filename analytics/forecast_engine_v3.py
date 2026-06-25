from __future__ import annotations

from pathlib import Path
import pandas as pd

V1 = Path("data/forecast_engine_v1.csv")
V2 = Path("data/forecast_engine_v2.csv")
OUT = Path("data/forecast_engine_v3.csv")
REPORT = Path("reports/forecast_engine_v3.md")

def read(path):
    return pd.read_csv(path) if path.exists() and path.stat().st_size > 1 else pd.DataFrame()

def main():
    v1 = read(V1)
    v2 = read(V2)

    if v1.empty and v2.empty:
        raise SystemExit("No forecast inputs found")

    if not v1.empty:
        v1["model_source"] = "v1_rule_based"
    if not v2.empty:
        v2["model_source"] = "v2_trend_based"

    combined = pd.concat([v1, v2], ignore_index=True, sort=False)

    combined["confidence"] = pd.to_numeric(combined["confidence"], errors="coerce").fillna(0)
    combined = combined.sort_values(["provider", "gpu", "confidence"], ascending=[True, True, False])

    champion = combined.groupby(["provider", "gpu"], dropna=False).head(1).copy()
    champion["model_name"] = "forecast_engine_v3"
    champion["selection_strategy"] = "highest_confidence_champion"
    champion["production_status"] = "candidate"

    OUT.parent.mkdir(exist_ok=True)
    REPORT.parent.mkdir(exist_ok=True)
    champion.to_csv(OUT, index=False)

    REPORT.write_text(
        f"# Forecast Engine v3\n\nRows: {len(champion)}\n\nv3 combines v1 and v2 forecasts and selects the highest-confidence provider/GPU champion.\n",
        encoding="utf-8",
    )

    print("FORECAST ENGINE V3")
    print("==================")
    print(f"Rows: {len(champion)}")
    print(f"CSV: {OUT}")

if __name__ == "__main__":
    main()
