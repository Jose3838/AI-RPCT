from datetime import date
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")

REQUIRED_COLUMNS = [
    "snapshot_date",
    "provider",
    "gpu",
    "region_code",
    "price_per_hour",
    "availability",
    "delivery_time_days",
    "source_url",
    "source_type",
    "claim_scope",
]


def read_csv(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def normalize(value):
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def is_present(value):
    return not pd.isna(value) and str(value).strip() != ""


def as_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def is_valid_snapshot_date(value, today=None):
    today = today or date.today()
    try:
        parsed = pd.to_datetime(value).date()
    except (TypeError, ValueError):
        return False
    return parsed <= today


def row_blockers(row, gpu_universe, provider_universe, region_universe, today=None):
    blockers = []
    for column in REQUIRED_COLUMNS:
        if not is_present(row.get(column)):
            blockers.append(f"missing_{column}")

    if blockers:
        return blockers

    if not is_valid_snapshot_date(row.get("snapshot_date"), today=today):
        blockers.append("invalid_or_future_snapshot_date")
    if normalize(row.get("provider")) not in provider_universe:
        blockers.append("unknown_provider")
    if normalize(row.get("gpu")) not in gpu_universe:
        blockers.append("unknown_gpu")
    if normalize(row.get("region_code")) not in region_universe:
        blockers.append("unknown_region")
    if as_float(row.get("price_per_hour")) is None or as_float(row.get("price_per_hour")) < 0:
        blockers.append("invalid_price_per_hour")
    if as_float(row.get("availability")) is None or as_float(row.get("availability")) < 0:
        blockers.append("invalid_availability")
    if as_float(row.get("delivery_time_days")) is None or as_float(row.get("delivery_time_days")) < 0:
        blockers.append("invalid_delivery_time_days")
    if not str(row.get("source_url", "")).startswith(("http://", "https://")):
        blockers.append("source_url_not_http")
    if row.get("source_type") != "manual_public_snapshot":
        blockers.append("source_type_must_be_manual_public_snapshot")
    if row.get("claim_scope") != "research_preview":
        blockers.append("claim_scope_must_be_research_preview")
    return blockers


def filter_valid_manual_snapshots(snapshots, gpu_universe, provider_universe, region_universe, today=None):
    if snapshots.empty:
        return snapshots.copy()

    gpu_names = {normalize(value) for value in gpu_universe.get("gpu", [])}
    provider_names = {normalize(value) for value in provider_universe.get("provider", [])}
    region_codes = {normalize(value) for value in region_universe.get("region_code", [])}

    valid_rows = []
    for _, row in snapshots.iterrows():
        if not row_blockers(row, gpu_names, provider_names, region_codes, today=today):
            valid_rows.append(row)

    if not valid_rows:
        return snapshots.iloc[0:0].copy()
    return pd.DataFrame(valid_rows)


def build_manual_snapshot_quality(data_dir=DATA_DIR, today=None):
    data_dir = Path(data_dir)
    snapshots = read_csv(data_dir / "manual_market_snapshots.csv")
    gpu_universe = read_csv(data_dir / "gpu_universe.csv")
    provider_universe = read_csv(data_dir / "provider_universe.csv")
    region_universe = read_csv(data_dir / "region_universe.csv")

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in snapshots.columns
    ]

    if snapshots.empty and not missing_columns:
        return pd.DataFrame([{
            "status": "no_snapshots",
            "snapshot_count": 0,
            "valid_snapshot_count": 0,
            "invalid_snapshot_count": 0,
            "duplicate_snapshot_count": 0,
            "source_labeled_count": 0,
            "claim_scope": "research_preview",
            "history_policy": "do_not_backfill_without_sources",
            "blockers": "add_manual_public_snapshots_with_sources",
            "next_action": "Add source-labeled manual public snapshots for priority GPUs, providers and regions.",
        }])

    invalid_count = 0
    source_labeled_count = 0
    blockers = set(missing_columns)
    gpu_names = {normalize(value) for value in gpu_universe.get("gpu", [])}
    provider_names = {normalize(value) for value in provider_universe.get("provider", [])}
    region_codes = {normalize(value) for value in region_universe.get("region_code", [])}

    for _, row in snapshots.iterrows():
        row_issues = row_blockers(row, gpu_names, provider_names, region_codes, today=today)
        if row_issues:
            invalid_count += 1
            blockers.update(row_issues)
        if is_present(row.get("source_url")) and row.get("source_type") == "manual_public_snapshot":
            source_labeled_count += 1

    duplicate_count = 0
    dedupe_columns = ["snapshot_date", "provider", "gpu", "region_code", "source_url"]
    if not snapshots.empty and all(column in snapshots.columns for column in dedupe_columns):
        duplicate_count = int(snapshots.duplicated(subset=dedupe_columns).sum())
        if duplicate_count:
            blockers.add("duplicate_snapshots")

    valid_count = max(0, len(snapshots) - invalid_count)
    if missing_columns:
        status = "schema_invalid"
    elif invalid_count or duplicate_count:
        status = "snapshots_need_cleanup"
    elif valid_count:
        status = "snapshots_valid_for_research_preview"
    else:
        status = "no_snapshots"

    if not blockers and valid_count:
        next_action = "Continue collecting source-labeled manual snapshots."
    else:
        next_action = "Fix manual snapshot blockers before counting them toward coverage."

    return pd.DataFrame([{
        "status": status,
        "snapshot_count": int(len(snapshots)),
        "valid_snapshot_count": int(valid_count),
        "invalid_snapshot_count": int(invalid_count),
        "duplicate_snapshot_count": duplicate_count,
        "source_labeled_count": int(source_labeled_count),
        "claim_scope": "research_preview",
        "history_policy": "do_not_backfill_without_sources",
        "blockers": ", ".join(sorted(blockers)) if blockers else "none",
        "next_action": next_action,
    }])


def main():
    result = build_manual_snapshot_quality()
    result.to_csv(DATA_DIR / "manual_snapshot_quality.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
