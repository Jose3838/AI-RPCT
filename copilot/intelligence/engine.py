from __future__ import annotations

from copilot.intelligence.actions import get_actions
from copilot.intelligence.capacity import get_capacity_layer
from copilot.intelligence.causal import get_causal_analysis
from copilot.intelligence.decision import get_decision_score
from copilot.intelligence.forecast import get_forecast_layer
from copilot.intelligence.historical import get_historical_layer
from copilot.intelligence.impact import get_impact_analysis
from copilot.intelligence.knowledge import get_knowledge
from copilot.intelligence.market import get_market_layer
from copilot.intelligence.pricing import get_pricing_layer
from copilot.intelligence.risk import get_risk_layer
from copilot.intelligence.scenario import run_scenario
from copilot.intelligence.simulation import simulate


def get_unified_intelligence() -> dict:
    historical = get_historical_layer()
    forecast = get_forecast_layer()
    capacity = get_capacity_layer()
    risk = get_risk_layer()
    pricing = get_pricing_layer()
    market = get_market_layer()
    impact = get_impact_analysis()
    causal = get_causal_analysis()
    scenario = run_scenario(
        variable="pricing",
        change=10,
    )
    simulation = simulate()

    intelligence = {
        "historical": historical,
        "forecast": forecast,
        "capacity": capacity,
        "risk": risk,
        "pricing": pricing,
        "market": market,
        "impact": impact,
        "causal": causal,
        "scenario_example": scenario,
        "simulation": simulation,
    }

    decision = get_decision_score(intelligence)

    intelligence["decision"] = decision
    intelligence["actions"] = get_actions(decision)
    intelligence["advisor"] = {
        "summary": {
            "status": "advisor available",
        }
    }
    intelligence["strategy"] = {
        "summary": {
            "status": "strategy available",
        }
    }
    intelligence["goals"] = {
        "summary": {
            "status": "goals available",
        }
    }
    intelligence["execution"] = {
        "summary": {
            "status": "execution available",
        }
    }
    intelligence["runtime"] = {
        "summary": {
            "status": "runtime available",
        }
    }
    intelligence["state"] = {
        "summary": {
            "status": "state available",
        }
    }
    intelligence["knowledge"] = get_knowledge()

    return intelligence
