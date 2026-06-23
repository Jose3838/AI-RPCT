from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def as_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_launch_controls(data_dir=DATA_DIR):
    path = Path(data_dir) / "launch_controls.csv"
    if not path.exists() or path.stat().st_size <= 1:
        return {}

    controls = {}
    for row in pd.read_csv(path).to_dict(orient="records"):
        control = row.get("control")
        if not control:
            continue
        controls[str(control).strip()] = as_bool(row.get("status", False))
    return controls


def next_action_for(blockers, preflight):
    if "provider_preflight_blocked" in blockers:
        return preflight.get("next_action", "Configure required provider API keys.")
    if "fallback_provenance_not_paid_safe" in blockers:
        return "Collect clean live-provider history before allowing paid beta claims."
    if "history_not_ready" in blockers:
        return "Run the core intelligence pipeline daily until 30 clean history days are collected."
    if "billing_not_ready" in blockers:
        return "Approve billing workflow before accepting paid customers."
    if "terms_not_ready" in blockers:
        return "Approve paid customer terms before accepting paid customers."
    if "paid_customers_disabled" in blockers:
        return "Enable paid customers only after all paid beta gates are green."
    if "core_not_paid_beta_ready" in blockers:
        return "Improve core signal quality before paid beta."
    return "Start controlled paid beta with one customer."


def build_paid_beta_gate(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    readiness = read_latest(data_dir / "core_intelligence_readiness.csv")
    quality = read_latest(data_dir / "core_signal_quality.csv")
    history = read_latest(data_dir / "core_history_audit.csv")
    provenance = read_latest(data_dir / "core_provenance_audit.csv")
    preflight = read_latest(data_dir / "provider_preflight_summary.csv")
    controls = read_launch_controls(data_dir)

    readiness_phase = readiness.get("readiness_phase", "unknown")
    paid_signal_ready = as_bool(readiness.get("paid_beta_signal_ready", False))
    provenance_band = provenance.get("provenance_band", "unknown")
    history_ready = as_bool(history.get("paid_beta_history_ready", False))
    preflight_blocked_count = as_float(
        readiness.get(
            "provider_preflight_blocked_count",
            preflight.get("blocked_count", 0),
        )
    )
    paid_claims_allowed = as_bool(
        provenance.get(
            "paid_claims_allowed",
            preflight.get("paid_reliability_claims_allowed", False),
        )
    )
    billing_ready = controls.get("billing_ready", False)
    terms_ready = controls.get("terms_ready", False)
    paid_customers_enabled = controls.get("paid_customers_allowed", False)

    blockers = []
    if readiness_phase != "paid_beta_ready" or not paid_signal_ready:
        blockers.append("core_not_paid_beta_ready")
    if not history_ready:
        blockers.append("history_not_ready")
    if provenance_band != "paid_claim_safe" or not paid_claims_allowed:
        blockers.append("fallback_provenance_not_paid_safe")
    if preflight_blocked_count > 0:
        blockers.append("provider_preflight_blocked")
    if not billing_ready:
        blockers.append("billing_not_ready")
    if not terms_ready:
        blockers.append("terms_not_ready")
    if not paid_customers_enabled:
        blockers.append("paid_customers_disabled")

    paid_beta_allowed = not blockers
    if paid_beta_allowed:
        gate_status = "ready"
    elif readiness_phase in {"usable_beta_signal", "building_history"} and preflight_blocked_count == 0:
        gate_status = "watch"
    else:
        gate_status = "blocked"

    return pd.DataFrame([{
        "paid_beta_allowed": paid_beta_allowed,
        "gate_status": gate_status,
        "readiness_phase": readiness_phase,
        "core_signal_quality_score": as_float(
            readiness.get(
                "core_signal_quality_score",
                quality.get("core_signal_quality_score"),
            )
        ),
        "history_progress_pct": as_float(history.get("progress_pct")),
        "history_days_remaining": as_float(history.get("days_remaining")),
        "provenance_band": provenance_band,
        "provider_preflight_blocked_count": preflight_blocked_count,
        "billing_ready": billing_ready,
        "terms_ready": terms_ready,
        "paid_customers_enabled": paid_customers_enabled,
        "blockers": ", ".join(blockers) if blockers else "none",
        "next_action": next_action_for(blockers, preflight),
    }])


def main():
    result = build_paid_beta_gate()
    result.to_csv(DATA_DIR / "paid_beta_gate.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
