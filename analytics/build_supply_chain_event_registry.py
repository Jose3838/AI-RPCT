from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "event_id",
    "event_date",
    "event_type",
    "title",
    "affected_vendors",
    "description",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
]

# Real, dated supply-chain / export-control events relevant to AI GPU
# infrastructure procurement risk. Deliberately covers only events with
# a specific, checkable date and an official or extensively-corroborated
# secondary source — not a comprehensive history, and not auto-updating
# (see notes in analytics/build_cloud_gpu_price_history.py for why static
# curated lists aren't wired into the scheduler).

ROWS = [
    {
        "event_id": "supply000001",
        "event_date": "2022-10-07",
        "event_type": "export_control",
        "title": "US BIS export controls on advanced computing/semiconductors to China (initial rule)",
        "affected_vendors": "NVIDIA, AMD, Intel",
        "description": (
            "US Bureau of Industry and Security (BIS) issued export controls "
            "restricting China's access to advanced computing chips and "
            "semiconductor manufacturing equipment. Chip-related rulings took "
            "effect 2022-10-07, with related manufacturing-assistance rulings "
            "effective 2022-10-12 and remaining rulings effective 2022-10-21."
        ),
        "source_url": "https://en.wikipedia.org/wiki/United_States_New_Export_Controls_on_Advanced_Computing_and_Semiconductors_to_China",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Multiple effective dates for different rule components; 2022-10-07 recorded as the initial/primary date. Verify exact provisions against the official BIS Federal Register rule before relying on this for a specific compliance decision.",
    },
    {
        "event_id": "supply000002",
        "event_date": "2023-10-17",
        "event_type": "export_control",
        "title": "US BIS strengthens and closes gaps in 2022 export controls",
        "affected_vendors": "NVIDIA, AMD",
        "description": (
            "BIS issued interim final rules updating the October 2022 "
            "controls, adding PRC entities to the Entity List and closing "
            "gaps that had allowed certain lower-threshold chip variants "
            "designed for the China market."
        ),
        "source_url": "https://www.congress.gov/crs-product/R48642",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Congressional Research Service summary; cross-referenced against CSIS analysis of the same rule.",
    },
    {
        "event_id": "supply000003",
        "event_date": "2024-12-01",
        "event_type": "export_control",
        "title": "US BIS expands controls; first country-wide HBM export restriction to China",
        "affected_vendors": "NVIDIA, AMD, SK Hynix, Samsung, Micron",
        "description": (
            "BIS expanded controls to cover additional semiconductor "
            "manufacturing equipment and chips, restricted exports to 16 "
            "additional PRC entities, and for the first time applied a "
            "country-wide restriction on exporting advanced HBM "
            "(High-Bandwidth Memory) to China."
        ),
        "source_url": "https://www.csis.org/analysis/understanding-biden-administrations-updated-export-controls",
        "source_type": "secondary_aggregated",
        "source_confidence": "low",
        "notes": "Day-level date not confirmed from a primary source in this pass; recorded as 2024-12-01 (month precision). Verify exact date against the official Federal Register rule before relying on it.",
    },
    {
        "event_id": "supply000004",
        "event_date": "2025-01-13",
        "event_type": "export_control_reversal",
        "title": "US Commerce Dept. loosens restrictions, permits H200/MI325X exports to China",
        "affected_vendors": "NVIDIA, AMD",
        "description": (
            "The Department of Commerce published a regulation permitting "
            "the sale of previously-restricted advanced AI chips (NVIDIA "
            "H200, AMD MI325X) to China, reversing part of the prior "
            "restriction regime."
        ),
        "source_url": "https://builtin.com/articles/trump-lifts-ai-chip-ban-china-nvidia",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Policy reversals in this area have moved quickly and repeatedly; treat this as a point-in-time record, not necessarily still current policy.",
    },
    {
        "event_id": "supply000005",
        "event_date": "2025-10-01",
        "event_type": "capacity_constraint",
        "title": "TSMC CoWoS advanced packaging capacity sold out through 2025 into 2026",
        "affected_vendors": "NVIDIA, AMD, TSMC",
        "description": (
            "TSMC CEO C.C. Wei stated during Q3 2025 earnings that CoWoS "
            "(the advanced packaging technology required to assemble modern "
            "GPU/AI accelerator dies) capacity was sold out through 2025 and "
            "into 2026. NVIDIA is reported to hold roughly 60% of available "
            "capacity."
        ),
        "source_url": "https://newsletter.semianalysis.com/p/ai-capacity-constraints-cowos-and",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Date recorded as approximate (Q3 2025 earnings season); exact call date not independently confirmed in this pass.",
    },
    {
        "event_id": "supply000006",
        "event_date": "2025-11-01",
        "event_type": "supply_agreement",
        "title": "SK Hynix reports entire 2026 HBM supply sold out",
        "affected_vendors": "SK Hynix, NVIDIA, AMD",
        "description": (
            "SK Hynix CFO Kim Jae-joon stated the company's entire 2026 HBM "
            "(High-Bandwidth Memory) production had already been sold out, "
            "underscoring HBM as the tightest single component constraint "
            "in AI accelerator supply chains."
        ),
        "source_url": "https://newsletter.semianalysis.com/p/ai-capacity-constraints-cowos-and",
        "source_type": "secondary_aggregated",
        "source_confidence": "low",
        "notes": "Exact statement date approximate; sourced via a secondary aggregator/newsletter rather than a direct SK Hynix earnings call transcript.",
    },
]


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(ROWS)


def main() -> None:
    data_path = ROOT / "data" / "supply_chain_event_registry.csv"
    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "supply_chain"
        / "supply_chain_event_registry.csv"
    )

    write_csv(data_path)
    write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} supply chain event records.")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
