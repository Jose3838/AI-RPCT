from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "paid_data_point_provenance.csv"


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


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def build_paid_data_point_provenance(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    methodologies = read_records(data_dir / "signal_methodology_registry.csv")
    provenance = read_latest(data_dir / "core_provenance_audit.csv")
    source_coverage = read_latest(data_dir / "source_url_coverage_metrics.csv")
    paid_gate = read_latest(data_dir / "paid_beta_gate.csv")

    rows = []
    for signal in methodologies:
        blockers = []
        if not as_bool(provenance.get("paid_claims_allowed")):
            blockers.append("core_provenance_not_paid_safe")
        if float(source_coverage.get("source_url_coverage_pct", 0) or 0) < 90:
            blockers.append("source_url_coverage_below_90_pct")
        if not as_bool(paid_gate.get("paid_beta_allowed")):
            blockers.append("paid_beta_gate_blocked")

        rows.append({
            "signal_id": signal.get("signal_id"),
            "signal_name": signal.get("signal_name"),
            "output_file": signal.get("output_file"),
            "primary_output": signal.get("primary_output"),
            "claim_scope": "paid_safe" if not blockers else "research_preview",
            "paid_safe": not blockers,
            "blockers": ", ".join(blockers) if blockers else "none",
            "evidence": "signal_methodology_registry|core_provenance_audit|source_url_coverage_metrics|paid_beta_gate",
        })

    if not rows:
        rows.append({
            "signal_id": "unknown",
            "signal_name": "unknown",
            "output_file": "",
            "primary_output": "",
            "claim_scope": "research_preview",
            "paid_safe": False,
            "blockers": "missing_signal_methodology_registry",
            "evidence": "data/signal_methodology_registry.csv",
        })
    return pd.DataFrame(rows)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_paid_data_point_provenance()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
