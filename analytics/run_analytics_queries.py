from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]

DB = ROOT / "warehouse" / "analytics" / "ai_rpct.duckdb"

OUTPUT = ROOT / "reports" / "analytics_queries.md"


def main():

    con = duckdb.connect(str(DB))

    feature_count = con.execute("""
        SELECT COUNT(*)
        FROM feature_store
    """).fetchone()[0]

    provider_count = con.execute("""
        SELECT COUNT(*)
        FROM provider_entity_registry
    """).fetchone()[0]

    accelerator_count = con.execute("""
        SELECT COUNT(*)
        FROM unified_accelerator_registry
    """).fetchone()[0]

    capacity_count = con.execute("""
        SELECT COUNT(*)
        FROM historical_capacity_registry
    """).fetchone()[0]

    con.close()

    lines = [
        "# AI-RPCT Analytics Report",
        "",
        "## Dataset Counts",
        "",
        f"- Feature Store: {feature_count}",
        f"- Providers: {provider_count}",
        f"- Accelerators: {accelerator_count}",
        f"- Capacity Records: {capacity_count}",
    ]

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print("Analytics report generated.")
    print(OUTPUT)


if __name__ == "__main__":
    main()
