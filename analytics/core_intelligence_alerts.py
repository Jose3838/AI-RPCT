from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "core_intelligence_alerts.csv"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def as_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def build_core_intelligence_alerts(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    stress = read_latest(data_dir / "ai_infrastructure_stress_index.csv")
    scarcity = read_latest(data_dir / "gpu_scarcity_index.csv")
    forecast = read_latest(data_dir / "forecast_signal.csv")
    dislocation = read_latest(data_dir / "price_dislocation_signal.csv")
    reliability = read_latest(data_dir / "provider_reliability_ranking.csv")

    alerts = []
    if as_float(stress.get("ai_infrastructure_stress_index")) >= 55:
        alerts.append({
            "alert_type": "stress_index_elevated",
            "severity": "high",
            "title": "AI infrastructure stress is elevated",
            "evidence": f"stress_index={stress.get('ai_infrastructure_stress_index')}",
            "recommended_action": "Review scarcity, forecast and provider reliability before making capacity commitments.",
        })
    if as_float(scarcity.get("gpu_scarcity_index")) >= 50:
        alerts.append({
            "alert_type": "gpu_scarcity_watch",
            "severity": "medium",
            "title": "GPU scarcity pressure is above watch threshold",
            "evidence": f"gpu_scarcity_index={scarcity.get('gpu_scarcity_index')}",
            "recommended_action": "Collect source-labeled price and availability snapshots for priority GPUs.",
        })
    if forecast.get("capacity_shock_band") in {"rising", "shock_up"}:
        alerts.append({
            "alert_type": "capacity_shock_rising",
            "severity": "high",
            "title": "Capacity shock signal is rising",
            "evidence": f"capacity_shock_band={forecast.get('capacity_shock_band')}",
            "recommended_action": "Check whether pressure persists in the next daily snapshot.",
        })
    if as_float(dislocation.get("price_dislocation_score")) >= 50:
        alerts.append({
            "alert_type": "price_dislocation_wide",
            "severity": "medium",
            "title": "Wide GPU price dislocation detected",
            "evidence": f"top_gpu={dislocation.get('top_gpu')}, score={dislocation.get('price_dislocation_score')}",
            "recommended_action": "Verify source URLs and track whether the spread persists.",
        })
    if as_float(reliability.get("reliability_score")) < 40 and reliability:
        alerts.append({
            "alert_type": "provider_reliability_critical",
            "severity": "high",
            "title": "Provider reliability leader is still weak",
            "evidence": f"provider={reliability.get('provider')}, score={reliability.get('reliability_score')}",
            "recommended_action": "Do not make paid reliability claims until live ingestion and history improve.",
        })

    if not alerts:
        alerts.append({
            "alert_type": "no_core_alerts",
            "severity": "low",
            "title": "No core intelligence alerts triggered",
            "evidence": "all thresholds below alert levels",
            "recommended_action": "Maintain daily collection cadence.",
        })

    return pd.DataFrame(alerts)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_core_intelligence_alerts()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
