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


def readiness_phase(quality, blocker_set):
    if as_bool(quality.get("paid_beta_signal_ready")):
        return "paid_beta_ready"
    if "restore_live_provider_ingestion" in blocker_set or "refresh_provider_connectors" in blocker_set:
        return "blocked_by_live_data"
    if "collect_30_days_of_core_signal_history" in blocker_set:
        return "building_history"
    if as_float(quality.get("core_signal_quality_score")) >= 65:
        return "usable_beta_signal"
    return "research_mode"


def build_core_intelligence_readiness():
    quality = read_latest(DATA_DIR / "core_signal_quality.csv")
    pulse = read_latest(DATA_DIR / "market_pulse_history.csv")
    ingestion = read_latest(DATA_DIR / "live_provider_ingestion_status.csv")

    blockers = [
        blocker.strip()
        for blocker in str(quality.get("blockers", "")).split(",")
        if blocker.strip() and blocker.strip() != "none"
    ]
    blocker_set = set(blockers)
    phase = readiness_phase(quality, blocker_set)

    if phase == "paid_beta_ready":
        next_action = "Start controlled paid beta with one customer."
    elif phase == "blocked_by_live_data":
        next_action = "Restore fresh provider ingestion for Vast and RunPod before making paid reliability claims."
    elif phase == "building_history":
        next_action = "Run the core intelligence pipeline daily until 30 clean history days are collected."
    else:
        next_action = "Keep improving signal quality before selling the intelligence layer."

    return pd.DataFrame([{
        "readiness_phase": phase,
        "core_signal_quality_score": as_float(quality.get("core_signal_quality_score")),
        "quality_band": quality.get("quality_band", "unknown"),
        "days_collected": as_float(quality.get("days_collected")),
        "high_provider_gap_count": as_float(quality.get("high_provider_gap_count")),
        "paid_beta_signal_ready": as_bool(quality.get("paid_beta_signal_ready")),
        "market_pulse_score": as_float(pulse.get("market_pulse_score")),
        "latest_ingestion_status": ingestion.get("status", "unknown"),
        "blockers": ", ".join(blockers) if blockers else "none",
        "next_action": next_action,
    }])


def main():
    result = build_core_intelligence_readiness()
    result.to_csv(DATA_DIR / "core_intelligence_readiness.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
