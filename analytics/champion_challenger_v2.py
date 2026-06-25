from __future__ import annotations

from pathlib import Path

import pandas as pd

COMPARISON = Path("data/model_comparison_v1.csv")
OUT = Path("data/champion_challenger_v2.csv")
REPORT = Path("reports/champion_challenger_v2.md")


def main() -> None:
    if not COMPARISON.exists() or COMPARISON.stat().st_size <= 1:
        raise SystemExit("model_comparison_v1.csv missing or empty")

    df = pd.read_csv(COMPARISON)

    df["avg_confidence"] = pd.to_numeric(df["avg_confidence"], errors="coerce").fillna(0)
    df["rows"] = pd.to_numeric(df["rows"], errors="coerce").fillna(0)
    df["learning_enabled"] = df["learning_enabled"].astype(str).str.lower().isin(["true", "1", "yes"])

    ranked = df.sort_values(
        ["learning_enabled", "avg_confidence", "rows"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    ranked["rank"] = ranked.index + 1
    ranked["role"] = "challenger"
    ranked.loc[0, "role"] = "champion"
    ranked["selection_policy"] = "learning_first_confidence_second_coverage_third"
    ranked["production_ready"] = ranked["role"] == "champion"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    ranked.to_csv(OUT, index=False)

    champion = ranked.iloc[0]

    REPORT.write_text(
        "\n".join(
            [
                "# Champion Challenger v2",
                "",
                f"Champion: {champion['model_name']}",
                f"Model type: {champion['model_type']}",
                f"Average confidence: {champion['avg_confidence']}",
                "",
                "## Policy",
                "",
                "1. Prefer learning-enabled models.",
                "2. Then prefer higher confidence.",
                "3. Then prefer broader coverage.",
                "",
                "## CTO Assessment",
                "",
                "Champion Challenger v2 promotes the strongest available forecast model into production-candidate status while keeping alternatives as challengers.",
                "This creates the operating model for future Forecast Engine versions.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("CHAMPION CHALLENGER V2")
    print("======================")
    print(ranked[["rank", "role", "model_name", "avg_confidence", "rows", "production_ready"]])


if __name__ == "__main__":
    main()
