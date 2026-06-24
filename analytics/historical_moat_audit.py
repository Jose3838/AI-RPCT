from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

WAREHOUSE_DIR = Path("warehouse")
DATA_OUT = Path("data/historical_moat_audit.csv")
REPORT_OUT = Path("reports/historical_moat_audit.md")

DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2}|20\d{6})")

FIELDS = [
    "domain",
    "file_count",
    "history_days",
    "first_date",
    "last_date",
    "history_depth_score",
    "moat_status",
    "notes",
]


def parse_date_from_path(path: Path) -> str | None:
    match = DATE_RE.search(str(path))
    if not match:
        return None

    raw = match.group(1)
    if "-" in raw:
        return raw

    return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"


def score_history_depth(history_days: int) -> tuple[int, str]:
    if history_days >= 90:
        return 100, "deep_historical_moat"
    if history_days >= 30:
        return 75, "strong_historical_moat"
    if history_days >= 7:
        return 50, "emerging_historical_moat"
    if history_days >= 2:
        return 25, "thin_historical_moat"
    if history_days == 1:
        return 10, "single_day_history"
    return 0, "no_history"


def collect_history() -> list[dict]:
    grouped: dict[str, list[str]] = defaultdict(list)

    for path in WAREHOUSE_DIR.rglob("*.csv"):
        if "__pycache__" in str(path):
            continue

        date_value = parse_date_from_path(path)
        if not date_value:
            continue

        domain = path.parent.name
        grouped[domain].append(date_value)

    rows = []

    for domain, dates in sorted(grouped.items()):
        unique_dates = sorted(set(dates))
        history_days = len(unique_dates)
        score, status = score_history_depth(history_days)

        rows.append(
            {
                "domain": domain,
                "file_count": len(dates),
                "history_days": history_days,
                "first_date": unique_dates[0],
                "last_date": unique_dates[-1],
                "history_depth_score": score,
                "moat_status": status,
                "notes": f"{domain} has {history_days} unique historical snapshot day(s).",
            }
        )

    return rows


def write_csv(rows: list[dict]) -> None:
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    with DATA_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict]) -> None:
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)

    total_domains = len(rows)
    avg_score = round(
        sum(int(r["history_depth_score"]) for r in rows) / total_domains, 2
    ) if total_domains else 0

    strongest = sorted(rows, key=lambda r: int(r["history_depth_score"]), reverse=True)

    lines = [
        "# Historical Moat Audit",
        "",
        f"Generated: {datetime.now(UTC).date().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Domains audited: {total_domains}",
        f"- Average history depth score: {avg_score}",
        "",
        "## Domains",
        "",
    ]

    for row in strongest:
        lines.append(
            f"- {row['domain']}: {row['history_days']} days, "
            f"score={row['history_depth_score']}, status={row['moat_status']}"
        )

    lines.extend(
        [
            "",
            "## CTO Assessment",
            "",
            "AI-RPCT has historical infrastructure, but moat depth is still early.",
            "The next commercial milestone is increasing history depth from scattered snapshots to daily continuity.",
            "",
            "## Next Actions",
            "",
            "1. Add daily snapshot cadence for warehouse domains.",
            "2. Track missing days per domain.",
            "3. Feed history_depth_score into evidence_moat_score_v3.",
            "4. Prioritize 30-day continuity before new API integrations.",
            "",
        ]
    )

    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = collect_history()
    write_csv(rows)
    write_report(rows)

    print("HISTORICAL MOAT AUDIT")
    print("=====================")
    print(f"Domains: {len(rows)}")
    print(f"CSV: {DATA_OUT}")
    print(f"Report: {REPORT_OUT}")


if __name__ == "__main__":
    main()
