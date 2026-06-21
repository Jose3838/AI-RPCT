from intelligence.signals.capacity_churn_index import (
    calculate_capacity_churn
)

def supply_shock_forecast():

    churn = calculate_capacity_churn()

    value = churn.get("capacity_churn", 0)

    if value >= 50:
        risk = "high"
    elif value >= 20:
        risk = "medium"
    else:
        risk = "low"

    return {
        "capacity_churn": value,
        "supply_shock_risk": risk
    }
