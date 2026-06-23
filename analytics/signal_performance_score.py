from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "signal_performance_score.csv"


def as_float(value, fallback=0.0):
    try:
        if pd.isna(value):
            return fallback
        return float(value)
    except (TypeError, ValueError):
        return fallback


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


def performance_band(score):
    if score >= 80:
        return "decision_grade"
    if score >= 60:
        return "usable_research"
    if score >= 40:
        return "building"
    return "thin"


def build_signal_performance_score():
    forecast_accuracy = read_latest(DATA_DIR / "forecast_accuracy.csv")
    cadence = read_latest(DATA_DIR / "collection_cadence_audit.csv")
    source_coverage = read_latest(DATA_DIR / "source_url_coverage_metrics.csv")
    quality = read_latest(DATA_DIR / "core_signal_quality.csv")
    provenance = read_records(DATA_DIR / "paid_data_point_provenance.csv")
    methodology = read_records(DATA_DIR / "signal_methodology_registry.csv")

    forecast_component = as_float(forecast_accuracy.get("directional_accuracy_pct"))
    cadence_component = min(100.0, as_float(cadence.get("days_collected")) / 30.0 * 100.0)
    source_component = as_float(source_coverage.get("source_url_coverage_pct"))
    quality_component = as_float(quality.get("core_signal_quality_score"))
    methodology_component = min(100.0, len(methodology) / 4.0 * 100.0)
    paid_safe_count = len([
        row for row in provenance
        if str(row.get("paid_safe", "")).lower() == "true"
    ])
    provenance_component = (paid_safe_count / len(provenance) * 100.0) if provenance else 0.0

    score = round(
        (forecast_component * 0.20)
        + (cadence_component * 0.20)
        + (source_component * 0.20)
        + (quality_component * 0.20)
        + (methodology_component * 0.10)
        + (provenance_component * 0.10),
        2,
    )

    blockers = []
    if cadence_component < 100:
        blockers.append("reach_30_clean_daily_records")
    if source_component < 90:
        blockers.append("increase_source_url_coverage")
    if forecast_component < 55:
        blockers.append("improve_or_wait_for_forecast_validation")
    if provenance_component < 100:
        blockers.append("make_paid_facing_points_paid_safe")

    return pd.DataFrame([{
        "signal_performance_score": score,
        "performance_band": performance_band(score),
        "forecast_accuracy_component": round(forecast_component, 2),
        "cadence_component": round(cadence_component, 2),
        "source_coverage_component": round(source_component, 2),
        "core_signal_quality_component": round(quality_component, 2),
        "methodology_component": round(methodology_component, 2),
        "provenance_component": round(provenance_component, 2),
        "documented_methodology_count": len(methodology),
        "paid_safe_signal_count": paid_safe_count,
        "tracked_signal_count": len(provenance),
        "blockers": ", ".join(blockers) if blockers else "none",
    }])


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_signal_performance_score()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
