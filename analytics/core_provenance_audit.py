from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "core_signal_history.csv"


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def build_core_provenance_audit(history_file=HISTORY_FILE):
    history_file = Path(history_file)
    if not history_file.exists() or history_file.stat().st_size <= 1:
        return pd.DataFrame([{
            "history_rows": 0,
            "research_only_rows": 0,
            "paid_claim_safe_rows": 0,
            "fallback_rows": 0,
            "fallback_row_pct": 0.0,
            "provenance_band": "missing",
            "paid_claims_allowed": False,
            "blockers": "missing_core_signal_history",
        }])

    history = pd.read_csv(history_file)
    if "history_claim_scope" not in history.columns:
        history["history_claim_scope"] = "research_only"
    if "provider_fallback_count" not in history.columns:
        history["provider_fallback_count"] = 0
    if "paid_reliability_claims_allowed" not in history.columns:
        history["paid_reliability_claims_allowed"] = False

    history["provider_fallback_count"] = pd.to_numeric(
        history["provider_fallback_count"],
        errors="coerce",
    ).fillna(0)

    history_rows = len(history)
    fallback_rows = int((history["provider_fallback_count"] > 0).sum())
    paid_safe_rows = int((history["history_claim_scope"] == "paid_claim_safe").sum())
    research_only_rows = history_rows - paid_safe_rows
    fallback_pct = round((fallback_rows / history_rows) * 100, 2) if history_rows else 0.0

    latest_paid_allowed = as_bool(history.iloc[-1].get("paid_reliability_claims_allowed")) if history_rows else False
    if latest_paid_allowed and fallback_rows == 0:
        provenance_band = "paid_claim_safe"
    elif fallback_rows:
        provenance_band = "fallback_contaminated"
    else:
        provenance_band = "research_only"

    blockers = []
    if fallback_rows:
        blockers.append("history_contains_provider_fallback_rows")
    if not latest_paid_allowed:
        blockers.append("latest_provider_preflight_blocks_paid_claims")

    return pd.DataFrame([{
        "history_rows": history_rows,
        "research_only_rows": research_only_rows,
        "paid_claim_safe_rows": paid_safe_rows,
        "fallback_rows": fallback_rows,
        "fallback_row_pct": fallback_pct,
        "provenance_band": provenance_band,
        "paid_claims_allowed": latest_paid_allowed and fallback_rows == 0,
        "blockers": ", ".join(blockers) if blockers else "none",
    }])


def main():
    audit = build_core_provenance_audit()
    audit.to_csv(DATA_DIR / "core_provenance_audit.csv", index=False)
    print(audit)


if __name__ == "__main__":
    main()
