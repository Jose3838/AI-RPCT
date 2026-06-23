from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "claim_gate_matrix.csv"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def build_claim_gate_matrix(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    paid_gate = read_latest(data_dir / "paid_beta_gate.csv")
    provenance = read_latest(data_dir / "core_provenance_audit.csv")
    forecast_accuracy = read_latest(data_dir / "forecast_accuracy.csv")
    source_coverage = read_latest(data_dir / "source_url_coverage_metrics.csv")
    scheduler = read_latest(data_dir / "collection_cadence_audit.csv")

    rows = [
        {
            "claim": "paid_live_reliability_claims",
            "allowed": as_bool(paid_gate.get("paid_beta_allowed")) and as_bool(provenance.get("paid_claims_allowed")),
            "scope": "paid_safe" if as_bool(provenance.get("paid_claims_allowed")) else "research_preview",
            "blockers": paid_gate.get("blockers", provenance.get("blockers", "unknown")),
            "evidence": "data/paid_beta_gate.csv|data/core_provenance_audit.csv",
        },
        {
            "claim": "forecast_predictive_claims",
            "allowed": as_bool(forecast_accuracy.get("paid_safe")),
            "scope": "paid_safe" if as_bool(forecast_accuracy.get("paid_safe")) else "research_preview",
            "blockers": "forecast_accuracy_not_paid_safe" if not as_bool(forecast_accuracy.get("paid_safe")) else "none",
            "evidence": "data/forecast_accuracy.csv",
        },
        {
            "claim": "region_coverage_claims",
            "allowed": float(source_coverage.get("source_url_coverage_pct", 0) or 0) >= 90,
            "scope": "research_preview",
            "blockers": "source_url_coverage_below_90_pct",
            "evidence": "data/source_url_coverage_metrics.csv",
        },
        {
            "claim": "daily_collection_cadence_claims",
            "allowed": scheduler.get("status") in {"building_history", "paid_beta_cadence_ready"},
            "scope": "research_preview",
            "blockers": "none" if scheduler.get("status") in {"building_history", "paid_beta_cadence_ready"} else "cadence_not_verified",
            "evidence": "data/collection_cadence_audit.csv",
        },
    ]
    return pd.DataFrame(rows)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_claim_gate_matrix()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
