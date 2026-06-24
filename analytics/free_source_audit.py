from __future__ import annotations

import csv
from pathlib import Path
from datetime import date

DATA_PATH = Path("data/free_source_audit.csv")
REPORT_PATH = Path("reports/free_source_audit_report.md")

FIELDS = [
    "source_name",
    "provider",
    "category",
    "claim_type",
    "collection_method",
    "requires_api",
    "public_access",
    "update_frequency",
    "reliability_score",
    "coverage_score",
    "evidence_ready",
    "moat_value",
    "notes",
]

FREE_SOURCES = [
    {
        "source_name": "runpod_public_marketplace",
        "provider": "runpod",
        "category": "marketplace",
        "claim_type": "gpu_price,gpu_availability",
        "collection_method": "public_page_or_html_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "daily",
        "reliability_score": 7,
        "coverage_score": 8,
        "evidence_ready": True,
        "moat_value": 9,
        "notes": "High-value GPU price and availability signal without mandatory API dependency.",
    },
    {
        "source_name": "vast_public_marketplace",
        "provider": "vast",
        "category": "marketplace",
        "claim_type": "gpu_price,gpu_availability,region_signal",
        "collection_method": "public_page_or_html_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "daily",
        "reliability_score": 7,
        "coverage_score": 9,
        "evidence_ready": True,
        "moat_value": 10,
        "notes": "Very strong market-price signal; API useful later but not required for initial moat.",
    },
    {
        "source_name": "lambda_gpu_cloud_catalog",
        "provider": "lambda",
        "category": "catalog",
        "claim_type": "gpu_support,gpu_availability,provider_region",
        "collection_method": "public_catalog_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "daily",
        "reliability_score": 8,
        "coverage_score": 7,
        "evidence_ready": True,
        "moat_value": 8,
        "notes": "Useful for catalog and availability claims.",
    },
    {
        "source_name": "coreweave_public_docs",
        "provider": "coreweave",
        "category": "docs",
        "claim_type": "gpu_support,provider_region,product_capability",
        "collection_method": "public_docs_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "weekly",
        "reliability_score": 8,
        "coverage_score": 7,
        "evidence_ready": True,
        "moat_value": 7,
        "notes": "Good for capability claims, weaker for live price claims.",
    },
    {
        "source_name": "ibm_cloud_gpu_docs",
        "provider": "ibm_cloud",
        "category": "docs",
        "claim_type": "gpu_support,provider_region",
        "collection_method": "public_docs_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "weekly",
        "reliability_score": 8,
        "coverage_score": 5,
        "evidence_ready": True,
        "moat_value": 6,
        "notes": "Important because ibm_cloud is an open provider gap.",
    },
    {
        "source_name": "voltage_park_public_site",
        "provider": "voltage_park",
        "category": "provider_site",
        "claim_type": "provider_capacity,gpu_support",
        "collection_method": "public_site_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "weekly",
        "reliability_score": 6,
        "coverage_score": 4,
        "evidence_ready": True,
        "moat_value": 7,
        "notes": "Important because voltage_park is an open provider gap; likely weaker live pricing signal.",
    },
    {
        "source_name": "nvidia_product_pages",
        "provider": "nvidia",
        "category": "vendor_docs",
        "claim_type": "gpu_specs,new_gpu_launch,gpu_generation",
        "collection_method": "public_docs_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "weekly",
        "reliability_score": 9,
        "coverage_score": 9,
        "evidence_ready": True,
        "moat_value": 8,
        "notes": "Authoritative source for GPU taxonomy and new GPU coverage gaps.",
    },
    {
        "source_name": "provider_status_pages",
        "provider": "multi_provider",
        "category": "status",
        "claim_type": "provider_outage,service_risk",
        "collection_method": "public_status_snapshot",
        "requires_api": False,
        "public_access": "public",
        "update_frequency": "hourly_or_daily",
        "reliability_score": 8,
        "coverage_score": 6,
        "evidence_ready": True,
        "moat_value": 8,
        "notes": "Useful for risk radar and customer decision layer.",
    },
]

def write_csv(rows: list[dict]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def write_report(rows: list[dict]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    total = len(rows)
    api_free = sum(1 for r in rows if not r["requires_api"])
    api_required = total - api_free
    evidence_ready = sum(1 for r in rows if r["evidence_ready"])
    avg_moat = round(sum(int(r["moat_value"]) for r in rows) / total, 2)

    top_sources = sorted(rows, key=lambda r: int(r["moat_value"]), reverse=True)[:5]

    lines = [
        "# Free Source Audit",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Total sources: {total}",
        f"- API-free sources: {api_free}",
        f"- API-required sources: {api_required}",
        f"- Evidence-ready sources: {evidence_ready}",
        f"- Average moat value: {avg_moat}",
        "",
        "## Top Moat Sources",
        "",
    ]

    for src in top_sources:
        lines.append(
            f"- {src['source_name']} ({src['provider']}): moat={src['moat_value']}, claims={src['claim_type']}"
        )

    lines.extend([
        "",
        "## CTO Assessment",
        "",
        "Sprint 31 confirms that AI-RPCT can build meaningful market intelligence without mandatory API keys.",
        "APIs remain valuable later for freshness, automation, and scale, but they are not required for the next moat-building phase.",
        "",
        "## Recommended Next Sprint",
        "",
        "Sprint 32 should focus on Historical Moat Acceleration: daily snapshots, source history, trend depth, and moat_score_v3.",
        "",
    ])

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    write_csv(FREE_SOURCES)
    write_report(FREE_SOURCES)

    print("FREE SOURCE AUDIT")
    print("=================")
    print(f"Sources: {len(FREE_SOURCES)}")
    print(f"API Free: {sum(1 for r in FREE_SOURCES if not r['requires_api'])}")
    print(f"CSV: {DATA_PATH}")
    print(f"Report: {REPORT_PATH}")

if __name__ == "__main__":
    main()
