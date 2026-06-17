from pathlib import Path
import pandas as pd
from datetime import datetime

DATA_DIR = Path("data")

HISTORY_FILES = {
    "gpu_scarcity": "gpu_scarcity_history.csv",
    "capacity_pressure": "capacity_pressure_history.csv",
    "provider_expansion": "provider_expansion_history.csv",
    "provider_momentum": "provider_momentum_history.csv",
    "risk_signal": "risk_signal_history.csv",
    "forecast": "forecast_history.csv",
}


def load_history(name: str) -> pd.DataFrame:
    file_path = DATA_DIR / HISTORY_FILES[name]

    if not file_path.exists():
        return pd.DataFrame()

    df = pd.read_csv(file_path)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df


def normalize_score(value, min_value=0, max_value=100):
    try:
        value = float(value)
    except Exception:
        return 0

    if max_value == min_value:
        return 0

    score = ((value - min_value) / (max_value - min_value)) * 100
    return max(0, min(100, round(score, 2)))


def latest_value(df: pd.DataFrame, column: str, default=0):
    if df.empty or column not in df.columns:
        return default

    df = df.dropna(subset=[column])

    if df.empty:
        return default

    if "timestamp" in df.columns:
        df = df.sort_values("timestamp")

    return df.iloc[-1][column]


def compute_market_regime():
    scarcity_df = load_history("gpu_scarcity")
    pressure_df = load_history("capacity_pressure")
    expansion_df = load_history("provider_expansion")

    scarcity = float(latest_value(scarcity_df, "scarcity_score", 0))
    pressure = float(latest_value(pressure_df, "capacity_pressure_score", 0))
    expansion = float(latest_value(expansion_df, "expansion_score", 0))

    composite = round((scarcity * 0.4) + (pressure * 0.4) + ((100 - expansion) * 0.2), 2)

    if composite >= 75:
        regime = "scarcity_event"
    elif composite >= 55:
        regime = "tight_capacity"
    elif expansion >= 70:
        regime = "expansion_cycle"
    elif composite <= 30:
        regime = "normal_capacity"
    else:
        regime = "transition_phase"

    return {
        "market_regime": regime,
        "regime_score": composite,
        "confidence": min(0.95, round(composite / 100 + 0.15, 2)),
        "drivers": {
            "gpu_scarcity": scarcity,
            "capacity_pressure": pressure,
            "provider_expansion": expansion,
        },
        "generated_at": datetime.utcnow().isoformat(),
    }


def compute_provider_relative_strength():
    momentum_df = load_history("provider_momentum")
    risk_df = load_history("risk_signal")

    if momentum_df.empty:
        return []

    provider_column = "provider"

    if provider_column not in momentum_df.columns:
        return []

    results = []

    for provider in momentum_df[provider_column].dropna().unique():
        provider_momentum = momentum_df[momentum_df[provider_column] == provider]

        momentum = float(latest_value(provider_momentum, "momentum_score", 0))

        risk = 0
        if not risk_df.empty and provider_column in risk_df.columns:
            provider_risk = risk_df[risk_df[provider_column] == provider]
            risk = float(latest_value(provider_risk, "risk_score", 0))

        strength = round((momentum * 0.7) + ((100 - risk) * 0.3), 2)

        results.append({
            "provider": provider,
            "relative_strength_score": strength,
            "momentum_score": momentum,
            "risk_score": risk,
        })

    return sorted(results, key=lambda x: x["relative_strength_score"], reverse=True)


def compute_provider_early_warning():
    momentum_df = load_history("provider_momentum")
    risk_df = load_history("risk_signal")

    if momentum_df.empty:
        return []

    warnings = []

    for provider in momentum_df["provider"].dropna().unique():
        provider_momentum = momentum_df[momentum_df["provider"] == provider].sort_values("timestamp")

        latest_momentum = float(latest_value(provider_momentum, "momentum_score", 0))

        previous_momentum = latest_momentum
        if len(provider_momentum) >= 2:
            previous_momentum = float(provider_momentum.iloc[-2].get("momentum_score", latest_momentum))

        momentum_delta = round(latest_momentum - previous_momentum, 2)

        risk_score = 0
        if not risk_df.empty and "provider" in risk_df.columns:
            provider_risk = risk_df[risk_df["provider"] == provider]
            risk_score = float(latest_value(provider_risk, "risk_score", 0))

        warning_score = round((risk_score * 0.6) + (max(0, -momentum_delta) * 2), 2)

        if warning_score >= 75:
            level = "critical"
        elif warning_score >= 50:
            level = "elevated"
        elif warning_score >= 25:
            level = "watch"
        else:
            level = "normal"

        warnings.append({
            "provider": provider,
            "warning_level": level,
            "warning_score": warning_score,
            "momentum_delta": momentum_delta,
            "risk_score": risk_score,
        })

    return sorted(warnings, key=lambda x: x["warning_score"], reverse=True)


def compute_forecast_attribution():
    forecast_df = load_history("forecast")
    scarcity_df = load_history("gpu_scarcity")
    pressure_df = load_history("capacity_pressure")
    expansion_df = load_history("provider_expansion")

    forecast_value = float(latest_value(forecast_df, "forecast_score", 0))
    scarcity = float(latest_value(scarcity_df, "scarcity_score", 0))
    pressure = float(latest_value(pressure_df, "capacity_pressure_score", 0))
    expansion = float(latest_value(expansion_df, "expansion_score", 0))

    total = max(1, scarcity + pressure + expansion)

    return {
        "forecast_score": forecast_value,
        "attribution": {
            "gpu_scarcity_weight": round((scarcity / total) * 100, 2),
            "capacity_pressure_weight": round((pressure / total) * 100, 2),
            "provider_expansion_weight": round((expansion / total) * 100, 2),
        },
        "drivers": {
            "gpu_scarcity": scarcity,
            "capacity_pressure": pressure,
            "provider_expansion": expansion,
        },
    }


def compute_market_signal_score():
    regime = compute_market_regime()
    relative_strength = compute_provider_relative_strength()
    warnings = compute_provider_early_warning()

    avg_strength = 0
    if relative_strength:
        avg_strength = sum(x["relative_strength_score"] for x in relative_strength) / len(relative_strength)

    avg_warning = 0
    if warnings:
        avg_warning = sum(x["warning_score"] for x in warnings) / len(warnings)

    market_signal_score = round(
        (regime["regime_score"] * 0.35)
        + (avg_strength * 0.4)
        + ((100 - avg_warning) * 0.25),
        2
    )

    if market_signal_score >= 80:
        direction = "strong_bullish"
    elif market_signal_score >= 65:
        direction = "bullish"
    elif market_signal_score >= 45:
        direction = "neutral"
    elif market_signal_score >= 30:
        direction = "bearish"
    else:
        direction = "stress"

    return {
        "market_signal_score": market_signal_score,
        "market_direction": direction,
        "market_regime": regime["market_regime"],
        "average_provider_strength": round(avg_strength, 2),
        "average_warning_score": round(avg_warning, 2),
        "generated_at": datetime.utcnow().isoformat(),
    }


def run_intelligence_snapshot_v4():
    return {
        "system": "AI-RPCT",
        "snapshot_version": "v4",
        "stage": "institutional_market_intelligence",
        "generated_at": datetime.utcnow().isoformat(),
        "market_regime": compute_market_regime(),
        "provider_relative_strength": compute_provider_relative_strength(),
        "provider_early_warning": compute_provider_early_warning(),
        "forecast_attribution": compute_forecast_attribution(),
        "market_signal": compute_market_signal_score(),
    }
