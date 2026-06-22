from pathlib import Path

import pandas as pd


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, float(value)))


def outlook_for(score):
    if score < 40:
        return "LOW RISK"
    if score < 70:
        return "ELEVATED RISK"
    return "HIGH RISK"


def shock_band(delta):
    if delta >= 20:
        return "shock_up"
    if delta >= 8:
        return "rising"
    if delta <= -20:
        return "shock_down"
    if delta <= -8:
        return "easing"
    return "stable"


def build_forecast_signal(rpct, shortage, scarcity=None):
    rpct = rpct.copy()
    rpct["score"] = pd.to_numeric(rpct["score"], errors="coerce").fillna(0)
    shortage_probability = float(pd.to_numeric(
        pd.Series([shortage.iloc[-1].get("shortage_probability", 0)]),
        errors="coerce"
    ).fillna(0).iloc[0])

    latest_score = float(rpct.iloc[-1]["score"]) if not rpct.empty else 0.0
    prior = rpct["score"].iloc[-8:-1]
    prior_baseline = float(prior.mean()) if not prior.empty else latest_score
    shock_delta = latest_score - prior_baseline
    shock_pressure = clamp(50 + (shock_delta * 1.5))

    scarcity_score = 0.0
    if scarcity is not None and not scarcity.empty:
        scarcity_score = float(pd.to_numeric(
            pd.Series([scarcity.iloc[-1].get("gpu_scarcity_index", 0)]),
            errors="coerce"
        ).fillna(0).iloc[0])

    forecast_score = round(clamp(
        (latest_score * 0.40)
        + (shortage_probability * 0.25)
        + (scarcity_score * 0.25)
        + (shock_pressure * 0.10)
    ), 2)

    history_depth = min(len(rpct), 30)
    confidence_score = round(clamp((history_depth / 30) * 70 + (30 if scarcity_score else 0)), 2)

    return pd.DataFrame([{
        "latest_rpct": round(latest_score, 2),
        "shortage_probability": round(shortage_probability, 2),
        "gpu_scarcity_index": round(scarcity_score, 2),
        "forecast_score": forecast_score,
        "outlook": outlook_for(forecast_score),
        "capacity_shock_delta": round(shock_delta, 2),
        "capacity_shock_band": shock_band(shock_delta),
        "confidence_score": confidence_score,
        "history_observations": int(len(rpct)),
    }])


def main():
    rpct = pd.read_csv("data/rpct_scores.csv")
    shortage = pd.read_csv("data/shortage_probability.csv")
    scarcity_path = Path("data/gpu_scarcity_index.csv")
    scarcity = pd.read_csv(scarcity_path) if scarcity_path.exists() else None

    result = build_forecast_signal(rpct, shortage, scarcity)
    result.to_csv("data/forecast_signal.csv", index=False)
    print(result)


if __name__ == "__main__":
    main()
