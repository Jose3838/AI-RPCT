from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


def latest_value(csv_path, column, default=0):
    path = Path(csv_path)

    if not path.exists():
        return default

    try:
        df = pd.read_csv(path)
        if df.empty:
            return default
        return float(df.iloc[-1].get(column, default))
    except Exception:
        return default


def level(value, high=70, medium=40):
    if value >= high:
        return "high"
    if value >= medium:
        return "medium"
    return "low"


def build_customer_decision_brief():
    scarcity_score = latest_value(
        "data/gpu_scarcity_index.csv",
        "gpu_scarcity_index"
    )

    price_dislocation_score = latest_value(
        "data/price_dislocation_signal.csv",
        "price_dislocation_score"
    )

    capacity_forecast_score = latest_value(
        "data/forecast_signal.csv",
        "forecast_score"
    )

    stress_score = latest_value(
        "data/ai_infrastructure_stress_index.csv",
        "ai_infrastructure_stress_index"
    )

    actions = []

    if scarcity_score >= 70:
        actions.append({
            "urgency": "high",
            "decision": "Secure GPU capacity within 14 days.",
            "why": "GPU scarcity indicators are elevated."
        })

    if price_dislocation_score >= 50:
        actions.append({
            "urgency": "medium",
            "decision": "Request multiple provider quotes before committing.",
            "why": "Price dislocation indicates meaningful spread between providers."
        })

    if capacity_forecast_score >= 60:
        actions.append({
            "urgency": "high",
            "decision": "Review capacity plan this week.",
            "why": "Capacity forecast risk is elevated."
        })

    if stress_score >= 75:
        actions.append({
            "urgency": "high",
            "decision": "Activate infrastructure contingency planning.",
            "why": "Overall AI infrastructure stress is critical."
        })

    if not actions:
        actions.append({
            "urgency": "low",
            "decision": "No urgent capacity action required.",
            "why": "Current market pressure indicators are not elevated."
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product_positioning": "AI-RPCT warns teams early about GPU shortages, price dislocations, and capacity risks.",
        "customer_value": "AI-RPCT helps organizations secure GPU capacity at lower cost and with lower risk.",
        "market_state": {
            "gpu_scarcity_index": scarcity_score,
            "gpu_scarcity_level": level(scarcity_score),
            "price_dislocation_score": price_dislocation_score,
            "price_dislocation_level": level(price_dislocation_score),
            "capacity_forecast_score": capacity_forecast_score,
            "capacity_forecast_level": level(capacity_forecast_score),
            "stress_index": stress_score,
            "stress_level": level(stress_score, high=75, medium=55)
        },
        "recommended_actions": actions
    }


def build_customer_decision_markdown():
    brief = build_customer_decision_brief()

    lines = [
        "# AI-RPCT Customer Decision Brief",
        "",
        f"**Positioning:** {brief['product_positioning']}",
        "",
        f"**Customer Value:** {brief['customer_value']}",
        "",
        "## Market State",
        "",
    ]

    for key, value in brief["market_state"].items():
        lines.append(f"- **{key}:** {value}")

    lines.extend([
        "",
        "## Recommended Actions",
        "",
    ])

    for action in brief["recommended_actions"]:
        lines.append(f"- **{action['urgency'].upper()}** — {action['decision']}")
        lines.append(f"  - Why: {action['why']}")

    return "\n".join(lines)
