from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "signal_explainability_drilldowns.csv"


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


def add_component(rows, signal, component, value, weight, interpretation, evidence_file):
    rows.append({
        "signal": signal,
        "component": component,
        "value": value,
        "weight": weight,
        "interpretation": interpretation,
        "evidence_file": evidence_file,
    })


def build_signal_explainability_drilldowns():
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    forecast = read_latest(DATA_DIR / "forecast_signal.csv")
    reliability = read_first(DATA_DIR / "provider_reliability_ranking.csv")
    dislocation = read_latest(DATA_DIR / "price_dislocation_signal.csv")
    stress = read_latest(DATA_DIR / "ai_infrastructure_stress_index.csv")
    performance = read_latest(DATA_DIR / "signal_performance_score.csv")

    rows = []
    add_component(rows, "gpu_scarcity_index", "availability_pressure_score", scarcity.get("availability_pressure_score"), 0.35, "Availability pressure captures how constrained tracked GPU capacity looks.", "data/gpu_scarcity_index.csv")
    add_component(rows, "gpu_scarcity_index", "price_pressure_score", scarcity.get("price_pressure_score"), 0.25, "Price pressure captures whether capacity is becoming expensive.", "data/gpu_scarcity_index.csv")
    add_component(rows, "gpu_scarcity_index", "frontier_pressure_score", scarcity.get("frontier_pressure_score"), 0.25, "Frontier pressure focuses on high-demand accelerator classes.", "data/gpu_scarcity_index.csv")
    add_component(rows, "gpu_scarcity_index", "provider_depth_score", scarcity.get("provider_depth_score"), 0.15, "Provider depth reduces false conviction from single-provider observations.", "data/gpu_scarcity_index.csv")

    add_component(rows, "capacity_shock_forecast", "latest_rpct", forecast.get("latest_rpct"), 0.40, "Latest RPCT captures current resource pressure.", "data/forecast_signal.csv")
    add_component(rows, "capacity_shock_forecast", "shortage_probability", forecast.get("shortage_probability"), 0.25, "Shortage probability adds forward-looking pressure.", "data/forecast_signal.csv")
    add_component(rows, "capacity_shock_forecast", "gpu_scarcity_index", forecast.get("gpu_scarcity_index"), 0.25, "Scarcity ties forecast risk back to observed GPU market pressure.", "data/forecast_signal.csv")
    add_component(rows, "capacity_shock_forecast", "capacity_shock_delta", forecast.get("capacity_shock_delta"), 0.10, "Shock delta measures abrupt movement versus recent baseline.", "data/forecast_signal.csv")

    add_component(rows, "provider_reliability_score", "freshness_score", reliability.get("freshness_score"), 0.20, "Freshness penalizes stale provider observations.", "data/provider_reliability_ranking.csv")
    add_component(rows, "provider_reliability_score", "depth_score", reliability.get("depth_score"), 0.10, "Depth measures how much provider evidence is present.", "data/provider_reliability_ranking.csv")
    add_component(rows, "provider_reliability_score", "availability_score", reliability.get("availability_score"), 0.10, "Availability score measures observed capacity depth.", "data/provider_reliability_ranking.csv")
    add_component(rows, "provider_reliability_score", "history_score", reliability.get("history_score"), 0.15, "History score rewards repeat observations over time.", "data/provider_reliability_ranking.csv")

    add_component(rows, "price_dislocation_signal", "price_dislocation_score", dislocation.get("price_dislocation_score"), 1.00, "Dislocation measures cross-provider price dispersion for comparable GPUs.", "data/price_dislocation_signal.csv")
    add_component(rows, "ai_infrastructure_stress_index", "ai_infrastructure_stress_index", stress.get("ai_infrastructure_stress_index"), 1.00, "Composite stress blends scarcity, forecast, dislocation and reliability pressure.", "data/ai_infrastructure_stress_index.csv")
    add_component(rows, "signal_performance_score", "signal_performance_score", performance.get("signal_performance_score"), 1.00, "Performance tracks whether the signal system is becoming more trustworthy over time.", "data/signal_performance_score.csv")

    return pd.DataFrame(rows)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    result = build_signal_explainability_drilldowns()
    result.to_csv(OUTPUT_FILE, index=False)
    print(result)


if __name__ == "__main__":
    main()
