from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COLUMNS = [
    "observation_id",
    "provider_id",
    "provider_name",
    "gpu_id",
    "instance_or_offer_name",
    "observation_date",
    "price_usd_per_gpu_hour",
    "pricing_tier",
    "normalization_note",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
]

# provider_id values match analytics/build_cloud_provider_registry_v2.py.
# ROWS below is a single hand-curated observation per provider, dated
# 2026-07-02. This is NOT wired into the Sprint 3 scheduler: ROWS is a
# static list, so an automated daily re-run would just no-op forever
# (append_or_write_csv dedupes by observation_id) without ever fetching a
# genuinely new price. Real ongoing collection would require live API/
# scraping integration per provider — future scope, not faked here by
# scheduling a job that re-writes the same numbers. To add a new
# observation, add a new dated row by hand (or build real per-provider
# fetchers) and re-run this script. Not a backfilled multi-year history
# either: cloud providers don't publish an archive of past on-demand
# rates the way GPU vendors publish spec sheets, so there is no credible
# way to reconstruct years of history retroactively.

ROWS = [
    {
        "observation_id": "cloudprice000001",
        "provider_id": "prov000001",
        "provider_name": "Amazon Web Services",
        "gpu_id": "gpu_nvidia_h100",
        "instance_or_offer_name": "p5.48xlarge (8x H100)",
        "observation_date": "2026-07-02",
        "price_usd_per_gpu_hour": "6.88",
        "pricing_tier": "on_demand_list",
        "normalization_note": "Full instance list price divided by 8 GPUs.",
        "source_url": "https://aws.amazon.com/ec2/instance-types/p5/",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "us-east-1 list price; other regions carry a surcharge. Figure via secondary aggregator citing AWS's public pricing, not independently re-derived from the raw AWS pricing API.",
    },
    {
        "observation_id": "cloudprice000002",
        "provider_id": "prov000003",
        "provider_name": "Google Cloud",
        "gpu_id": "gpu_nvidia_h100",
        "instance_or_offer_name": "a3-highgpu-8g (8x H100)",
        "observation_date": "2026-07-02",
        "price_usd_per_gpu_hour": "10.98",
        "pricing_tier": "on_demand_list",
        "normalization_note": "Full instance list price divided by 8 GPUs.",
        "source_url": "https://cloud.google.com/compute/gpus-pricing",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "us-central1 list price as of ~2026-05-22 per secondary source; not independently re-verified against the live GCP pricing calculator on the observation date.",
    },
    {
        "observation_id": "cloudprice000003",
        "provider_id": "prov000002",
        "provider_name": "Microsoft Azure",
        "gpu_id": "gpu_nvidia_h100",
        "instance_or_offer_name": "Standard_ND96isr_H100_v5 (8x H100)",
        "observation_date": "2026-07-02",
        "price_usd_per_gpu_hour": "12.29",
        "pricing_tier": "on_demand_list",
        "normalization_note": "Full instance list price divided by 8 GPUs.",
        "source_url": "https://instances.vantage.sh/azure/vm/nd96isrh100-v5",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "East US list price as of ~2026-05-21 per secondary source; not independently re-verified against the live Azure pricing calculator on the observation date.",
    },
    {
        "observation_id": "cloudprice000004",
        "provider_id": "prov000004",
        "provider_name": "CoreWeave",
        "gpu_id": "gpu_nvidia_h100",
        "instance_or_offer_name": "HGX H100 8-GPU node",
        "observation_date": "2026-07-02",
        "price_usd_per_gpu_hour": "6.16",
        "pricing_tier": "on_demand_list",
        "normalization_note": "$49.24/hr full-node list price divided by 8 GPUs.",
        "source_url": "https://www.coreweave.com/pricing",
        "source_type": "official_pricing_page",
        "source_confidence": "high",
        "notes": "Directly fetched from CoreWeave's own public pricing page on the observation date. North America region.",
    },
    {
        "observation_id": "cloudprice000005",
        "provider_id": "prov000005",
        "provider_name": "Lambda",
        "gpu_id": "gpu_nvidia_h100",
        "instance_or_offer_name": "H100 (Community Cloud)",
        "observation_date": "2026-07-02",
        "price_usd_per_gpu_hour": "2.99",
        "pricing_tier": "on_demand_list",
        "normalization_note": "Listed directly as a per-GPU-hour rate, no normalization needed.",
        "source_url": "https://lambda.ai/service/gpu-cloud",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Via secondary aggregator citing Lambda's public rate card; not independently re-fetched from Lambda's own page on the observation date.",
    },
    {
        "observation_id": "cloudprice000006",
        "provider_id": "prov000008",
        "provider_name": "RunPod",
        "gpu_id": "gpu_nvidia_h100",
        "instance_or_offer_name": "H100 (Community Cloud)",
        "observation_date": "2026-07-02",
        "price_usd_per_gpu_hour": "1.99",
        "pricing_tier": "on_demand_list",
        "normalization_note": "Listed directly as a per-GPU-hour rate, no normalization needed. Secure Cloud tier is separately reported at $2.39/hr.",
        "source_url": "https://www.runpod.io/pricing",
        "source_type": "secondary_aggregated",
        "source_confidence": "medium",
        "notes": "Via secondary aggregator citing RunPod's public rate card; not independently re-fetched from RunPod's own page on the observation date.",
    },
]


def append_or_write_csv(path: Path) -> None:
    """Append new observations to existing history, or create the file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    existing_rows = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))

    existing_ids = {row["observation_id"] for row in existing_rows}
    new_rows = [row for row in ROWS if row["observation_id"] not in existing_ids]

    all_rows = existing_rows + new_rows

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)


def main() -> None:
    data_path = ROOT / "data" / "cloud_gpu_price_history.csv"
    warehouse_path = (
        ROOT
        / "warehouse"
        / "historical"
        / "providers"
        / "cloud_gpu_price_history.csv"
    )

    append_or_write_csv(data_path)
    append_or_write_csv(warehouse_path)

    print(f"Wrote {len(ROWS)} cloud GPU price observations (deduplicated by observation_id).")
    print(data_path)
    print(warehouse_path)


if __name__ == "__main__":
    main()
