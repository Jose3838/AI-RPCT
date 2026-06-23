from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "source_backed_scarcity.csv"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def build_source_backed_scarcity():
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    evidence = read_records(DATA_DIR / "source_evidence_view.csv")
    source_coverage = read_latest(DATA_DIR / "source_url_coverage_metrics.csv")
    linked_rows = [
        row for row in evidence
        if str(row.get("evidence_quality", "")).lower() == "linked"
    ]
    missing_rows = [
        row for row in evidence
        if str(row.get("evidence_quality", "")).lower() == "missing"
    ]
    needs_url_rows = [
        row for row in evidence
        if str(row.get("evidence_quality", "")).lower() == "needs_url"
    ]

    if not scarcity:
        status = "missing_scarcity_index"
    elif linked_rows:
        status = "source_backed"
    elif evidence and not missing_rows:
        status = "observed_needs_source_urls"
    else:
        status = "needs_manual_source_snapshots"

    return pd.DataFrame([{
        "status": status,
        "gpu_scarcity_index": scarcity.get("gpu_scarcity_index", 0),
        "scarcity_band": scarcity.get("scarcity_band", "unknown"),
        "source_url_coverage_pct": source_coverage.get("source_url_coverage_pct", 0),
        "source_evidence_rows": len(evidence),
        "linked_source_rows": len(linked_rows),
        "needs_url_rows": len(needs_url_rows),
        "paid_claim_safe": status == "source_backed" and float(source_coverage.get("source_url_coverage_pct", 0) or 0) >= 90,
        "next_action": "maintain_daily_source_collection" if linked_rows else "collect_source_labeled_gpu_snapshots",
        "evidence_file": "data/source_evidence_view.csv",
    }])


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_source_backed_scarcity()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
