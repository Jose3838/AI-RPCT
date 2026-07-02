from __future__ import annotations

from copilot.io import load_csv

# Sprint 6 Procurement Optimizer: cloud vs. on-prem breakeven, using only
# GPUs where this repo has both a real purchase-price anchor
# (historical_pricing_registry.csv) and real cloud hourly rates
# (cloud_gpu_price_history.csv) - currently only H100.
#
# This is a static financial calculation from two real data points, NOT
# a forecast: it deliberately does not try to predict future price
# movement (the underlying time series are too short for that - see
# project_decision_intelligence_sprint6 memory). It also deliberately
# does NOT include power, cooling, facility, staffing, or depreciation
# costs for the on-prem side, or financing costs - those would need
# real inputs this repo doesn't have. Treat the breakeven-hours figure
# as a lower bound on how long on-prem needs to be used to match the
# sticker price of buying the hardware, not a complete TCO comparison.

_HOURS_PER_MONTH_FULL_TIME = 730  # 24/7 utilization
_HOURS_PER_MONTH_BUSINESS = 22 * 8  # ~22 working days, 8h/day


def _load_h100_purchase_price():
    pricing_rows = load_csv("data/historical_pricing_registry.csv")

    h100_rows = [
        row for row in pricing_rows
        if row.get("relationship_id") == "rel000014"
    ]

    if not h100_rows:
        return None

    return {
        "price_usd": float(h100_rows[0]["price_amount"]),
        "observation_date": h100_rows[0]["observation_date"],
        "verification_status": h100_rows[0]["verification_status"],
    }


def _load_h100_cloud_rates():
    cloud_rows = load_csv("data/cloud_gpu_price_history.csv")

    return [
        {
            "provider_name": row["provider_name"],
            "price_usd_per_gpu_hour": float(row["price_usd_per_gpu_hour"]),
            "instance_or_offer_name": row["instance_or_offer_name"],
            "source_confidence": row["source_confidence"],
        }
        for row in cloud_rows
        if row.get("gpu_id") == "gpu_nvidia_h100"
    ]


def get_procurement_optimizer() -> dict:
    purchase = _load_h100_purchase_price()
    cloud_rates = _load_h100_cloud_rates()

    if not purchase or not cloud_rates:
        return {
            "status": "insufficient data",
            "message": "Need both an on-prem purchase price and at least one cloud rate for the same GPU.",
        }

    comparisons = []

    for rate in sorted(cloud_rates, key=lambda r: r["price_usd_per_gpu_hour"]):
        breakeven_hours = purchase["price_usd"] / rate["price_usd_per_gpu_hour"]

        comparisons.append({
            "provider_name": rate["provider_name"],
            "cloud_price_usd_per_gpu_hour": rate["price_usd_per_gpu_hour"],
            "breakeven_hours": round(breakeven_hours, 1),
            "breakeven_months_full_time_utilization": round(
                breakeven_hours / _HOURS_PER_MONTH_FULL_TIME, 1
            ),
            "breakeven_months_business_hours_utilization": round(
                breakeven_hours / _HOURS_PER_MONTH_BUSINESS, 1
            ),
            "source_confidence": rate["source_confidence"],
        })

    cheapest = comparisons[0]
    most_expensive = comparisons[-1]

    recommendation = (
        f"For sustained (24/7) utilization beyond "
        f"~{cheapest['breakeven_months_full_time_utilization']} months, "
        f"buying outright breaks even faster than the cheapest observed "
        f"cloud rate ({cheapest['provider_name']}). For intermittent/"
        f"business-hours-only workloads, cloud remains cheaper for much "
        f"longer (~{cheapest['breakeven_months_business_hours_utilization']} "
        f"months to break even at the same rate) since on-prem hardware "
        f"sits idle outside those hours while still requiring the same "
        f"upfront investment."
    )

    return {
        "status": "ok",
        "gpu": "NVIDIA H100",
        "on_prem_purchase_price_usd": purchase["price_usd"],
        "on_prem_price_observation_date": purchase["observation_date"],
        "on_prem_price_confidence": purchase["verification_status"],
        "cloud_comparisons": comparisons,
        "cheapest_cloud_option": cheapest,
        "most_expensive_cloud_option": most_expensive,
        "recommendation": recommendation,
        "caveats": [
            "Breakeven ignores power, cooling, facility, staffing, financing, "
            "and depreciation costs for the on-prem side - a complete TCO "
            "comparison would need those inputs.",
            "The on-prem purchase price is a 2023 launch-era estimate "
            "(verification_status: partial), not a current street price; "
            "actual current purchase cost may differ significantly.",
            "Cloud rates are a single-day snapshot (2026-07-02), not a "
            "time series - they will drift as providers change pricing.",
        ],
    }
