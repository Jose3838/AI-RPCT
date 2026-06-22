from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "core_signal_history.csv"


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_first(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[0].to_dict()


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_core_signal_history_row(generated_at=None):
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    forecast = read_latest(DATA_DIR / "forecast_signal.csv")
    reliability = read_first(DATA_DIR / "provider_reliability_ranking.csv")
    quality = read_latest(DATA_DIR / "live_data_quality_score.csv")
    preflight_summary = read_latest(DATA_DIR / "provider_preflight_summary.csv")
    ingestion_rows = read_records(DATA_DIR / "live_provider_ingestion_status.csv")

    ingestion_statuses = sorted({str(row.get("status", "unknown")) for row in ingestion_rows}) or ["unknown"]
    fallback_count = len([row for row in ingestion_rows if as_bool(row.get("used_fallback"))])
    paid_reliability_allowed = as_bool(preflight_summary.get("paid_reliability_claims_allowed"))

    return {
        "timestamp": generated_at,
        "date": generated_at[:10],
        "gpu_scarcity_index": as_float(scarcity.get("gpu_scarcity_index")),
        "scarcity_band": scarcity.get("scarcity_band", "unknown"),
        "availability_pressure_score": as_float(scarcity.get("availability_pressure_score")),
        "price_pressure_score": as_float(scarcity.get("price_pressure_score")),
        "frontier_pressure_score": as_float(scarcity.get("frontier_pressure_score")),
        "provider_depth_score": as_float(scarcity.get("provider_depth_score")),
        "capacity_forecast_score": as_float(forecast.get("forecast_score")),
        "capacity_outlook": forecast.get("outlook", "unknown"),
        "capacity_shock_delta": as_float(forecast.get("capacity_shock_delta")),
        "capacity_shock_band": forecast.get("capacity_shock_band", "unknown"),
        "forecast_confidence_score": as_float(forecast.get("confidence_score")),
        "top_reliability_provider": reliability.get("provider", "unknown"),
        "top_provider_reliability_score": as_float(reliability.get("reliability_score")),
        "top_provider_reliability_band": reliability.get("reliability_band", "unknown"),
        "live_data_quality_score": as_float(quality.get("live_data_quality_score")),
        "provider_ingestion_statuses": "|".join(ingestion_statuses),
        "provider_fallback_count": fallback_count,
        "paid_reliability_claims_allowed": paid_reliability_allowed,
        "history_claim_scope": "paid_claim_safe" if paid_reliability_allowed else "research_only",
    }


def append_core_signal_history(history_file=HISTORY_FILE, generated_at=None):
    row = pd.DataFrame([build_core_signal_history_row(generated_at)])
    history_file = Path(history_file)
    history_file.parent.mkdir(exist_ok=True)

    if history_file.exists() and history_file.stat().st_size > 1:
        history = pd.read_csv(history_file)
        history = pd.concat([history, row], ignore_index=True)
        history = history.drop_duplicates(subset=["date"], keep="last")
    else:
        history = row

    history.to_csv(history_file, index=False)
    latest = history.iloc[-1].to_dict()

    return {
        "status": "saved",
        "file": str(history_file),
        "record_count": int(len(history)),
        "latest": latest,
    }


def build_core_signal_history_summary(history_file=HISTORY_FILE):
    history_file = Path(history_file)
    if not history_file.exists() or history_file.stat().st_size <= 1:
        return {
            "record_count": 0,
            "days_collected": 0,
            "latest": {},
            "previous": {},
            "deltas": {},
            "coverage_band": "none",
        }

    history = pd.read_csv(history_file)
    latest = history.iloc[-1].to_dict()
    previous = history.iloc[-2].to_dict() if len(history) > 1 else {}
    days_collected = history["date"].nunique() if "date" in history.columns else len(history)

    deltas = {}
    for key in [
        "gpu_scarcity_index",
        "capacity_forecast_score",
        "top_provider_reliability_score",
        "live_data_quality_score",
        "provider_fallback_count",
    ]:
        deltas[key] = round(
            as_float(latest.get(key)) - as_float(previous.get(key)),
            2
        ) if previous else 0.0

    if days_collected >= 30:
        coverage_band = "paid_beta_ready"
    elif days_collected >= 14:
        coverage_band = "forming_moat"
    elif days_collected >= 7:
        coverage_band = "early_signal"
    else:
        coverage_band = "thin_history"

    return {
        "record_count": int(len(history)),
        "days_collected": int(days_collected),
        "latest": latest,
        "previous": previous,
        "deltas": deltas,
        "coverage_band": coverage_band,
    }


def main():
    payload = append_core_signal_history()
    print(payload)


if __name__ == "__main__":
    main()
