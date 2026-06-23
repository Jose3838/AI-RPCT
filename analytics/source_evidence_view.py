from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "source_evidence_view.csv"
SNAPSHOT_FILE = DATA_DIR / "manual_market_snapshots.csv"


EXPECTED_COLUMNS = [
    "observed_at",
    "provider",
    "gpu",
    "region_code",
    "source_type",
    "source_url",
    "price_per_hour",
    "availability",
    "delivery_time_hours",
    "claim_scope",
]


def build_source_evidence_view(snapshot_file=SNAPSHOT_FILE):
    missing_row = {
        "status": "no_source_evidence",
        "observed_at": "",
        "provider": "",
        "gpu": "",
        "region_code": "",
        "source_type": "",
        "source_url": "",
        "price_per_hour": "",
        "availability": "",
        "delivery_time_hours": "",
        "claim_scope": "research_preview",
        "evidence_quality": "missing",
        "next_action": "Add source-labeled rows to data/manual_market_snapshots.csv",
    }
    path = Path(snapshot_file)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame([missing_row])

    snapshots = pd.read_csv(path)
    if snapshots.empty:
        return pd.DataFrame([missing_row])
    for column in EXPECTED_COLUMNS:
        if column not in snapshots.columns:
            snapshots[column] = ""

    evidence = snapshots[EXPECTED_COLUMNS].copy()
    evidence["status"] = "source_evidence_available"
    evidence["has_source_url"] = evidence["source_url"].astype(str).str.startswith(("http://", "https://"))
    evidence["evidence_quality"] = evidence["has_source_url"].map(lambda value: "linked" if value else "needs_url")
    evidence["next_action"] = evidence["has_source_url"].map(
        lambda value: "maintain_daily_collection" if value else "add_source_url_before_paid_claims"
    )
    evidence = evidence.sort_values(["observed_at", "provider", "gpu"], ascending=[False, True, True])
    return evidence[[
        "status",
        "observed_at",
        "provider",
        "gpu",
        "region_code",
        "source_type",
        "source_url",
        "price_per_hour",
        "availability",
        "delivery_time_hours",
        "claim_scope",
        "evidence_quality",
        "next_action",
    ]]


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_source_evidence_view()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result.head(20))


if __name__ == "__main__":
    main()
