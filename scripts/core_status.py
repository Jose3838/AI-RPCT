import json
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_records(path, limit=5):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).head(limit).to_dict(orient="records")


def build_core_status():
    readiness = read_latest(DATA_DIR / "core_intelligence_readiness.csv")
    quality = read_latest(DATA_DIR / "core_signal_quality.csv")
    pulse = read_latest(DATA_DIR / "market_pulse_history.csv")
    gaps = read_records(DATA_DIR / "provider_reliability_gaps.csv", limit=5)

    return {
        "product": "AI-RPCT",
        "readiness_phase": readiness.get("readiness_phase", "unknown"),
        "core_signal_quality_score": readiness.get("core_signal_quality_score", quality.get("core_signal_quality_score")),
        "quality_band": readiness.get("quality_band", quality.get("quality_band", "unknown")),
        "market_pulse_score": readiness.get("market_pulse_score", pulse.get("market_pulse_score")),
        "paid_beta_signal_ready": readiness.get("paid_beta_signal_ready", False),
        "blockers": readiness.get("blockers", quality.get("blockers", "unknown")),
        "next_action": readiness.get("next_action", "Run ./scripts/run_core_intelligence.sh"),
        "top_provider_gaps": gaps,
    }


def main():
    print(json.dumps(build_core_status(), indent=2, default=str))


if __name__ == "__main__":
    main()
