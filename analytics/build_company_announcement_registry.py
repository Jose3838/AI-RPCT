from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "announcement_id",
    "company",
    "announcement_date",
    "announcement_type",
    "title",
    "figure_usd_billion",
    "description",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
]

# Major hyperscaler AI infrastructure capex guidance for 2026, as reported
# during Q4 2025 / early-2026 earnings calls. These are demand-side
# signals for GPU/AI infrastructure investment (relevant to this
# platform's stated Investment/Capacity Intelligence questions), not a
# comprehensive corporate-announcement feed. Figures come from secondary
# financial press synthesis of the underlying earnings calls/SEC
# filings; exact call dates and any subsequent guidance revisions were
# not independently verified against each company's own investor
# relations page in this pass, hence source_confidence: medium
# throughout, not high.

ROWS = [
    {
        "announcement_id": "company000001",
        "company": "Amazon (AWS)",
        "announcement_date": "2026-02-01",
        "announcement_type": "capex_guidance",
        "title": "Amazon reiterates ~$200B 2026 capex guidance",
        "figure_usd_billion": "200",
        "description": (
            "Amazon guided approximately $200 billion in 2026 capital "
            "expenditures, the large majority directed at AI/data center "
            "infrastructure (GPU clusters, custom silicon, data centers). "
            "Guidance held steady from its initial February estimate "
            "through subsequent quarters."
        ),
        "source_url": "https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Date recorded as approximate (February 2026 earnings window); not independently verified against Amazon's own investor relations filing.",
    },
    {
        "announcement_id": "company000002",
        "company": "Alphabet (Google Cloud)",
        "announcement_date": "2026-04-29",
        "announcement_type": "capex_guidance",
        "title": "Alphabet raises 2026 capex guidance to $175-185B",
        "figure_usd_billion": "180",
        "description": (
            "Alphabet raised its 2026 capital expenditure forecast to a "
            "range of $175-185 billion, up from earlier guidance, citing "
            "AI infrastructure demand. Figure recorded here as the "
            "midpoint of the guided range."
        ),
        "source_url": "https://fortune.com/2026/04/29/microsoft-meta-google-ai-capex-spending-billions/",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Range midpoint used for figure_usd_billion; actual guidance is a range ($175-185B), not a single point figure.",
    },
    {
        "announcement_id": "company000003",
        "company": "Microsoft (Azure)",
        "announcement_date": "2026-04-29",
        "announcement_type": "capex_guidance",
        "title": "Microsoft guides toward ~$190B 2026 capex",
        "figure_usd_billion": "190",
        "description": (
            "Microsoft's 2026 capital expenditure guidance tracked toward "
            "approximately $190 billion, with AI/cloud infrastructure "
            "(Azure GPU capacity) as the primary driver."
        ),
        "source_url": "https://fortune.com/2026/04/29/microsoft-meta-google-ai-capex-spending-billions/",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Date recorded as approximate (same reporting window as the Alphabet/Meta figures above).",
    },
    {
        "announcement_id": "company000004",
        "company": "Meta",
        "announcement_date": "2026-04-29",
        "announcement_type": "capex_guidance",
        "title": "Meta raises 2026 capex guidance to $115-135B",
        "figure_usd_billion": "125",
        "description": (
            "Meta raised its 2026 capital expenditure guidance to a range "
            "of $115-135 billion, driven by AI infrastructure and data "
            "center investment. Figure recorded here as the midpoint of "
            "the guided range."
        ),
        "source_url": "https://fortune.com/2026/04/29/microsoft-meta-google-ai-capex-spending-billions/",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Range midpoint used for figure_usd_billion; actual guidance is a range ($115-135B), not a single point figure.",
    },
    {
        "announcement_id": "company000005",
        "company": "Amazon, Alphabet, Meta, Microsoft (combined)",
        "announcement_date": "2026-02-06",
        "announcement_type": "market_aggregate",
        "title": "Combined 2026 hyperscaler AI capex reaches ~$725B, up 77% YoY",
        "figure_usd_billion": "725",
        "description": (
            "Aggregate 2026 capital expenditure guidance across the four "
            "hyperscalers reached approximately $725 billion, up from "
            "roughly $410 billion in 2025 (a ~77% year-over-year "
            "increase), with the large majority directed at AI "
            "infrastructure (GPU clusters, custom silicon, data center "
            "construction)."
        ),
        "source_url": "https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Aggregate figure synthesized by secondary financial press from the four companies' individual guidance; not independently re-summed from each company's own filing in this pass.",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "company_announcement_registry.csv"
    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "company_announcements"
        / "company_announcement_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} company announcement records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
