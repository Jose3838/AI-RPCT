def build_intelligence_registry():
    return {
        "status": "ok",
        "version": "v1",
        "intelligence_models": [
            {
                "name": "Data Trust Index",
                "category": "data_quality"
            },
            {
                "name": "GPU Scarcity Index",
                "category": "market_intelligence"
            },
            {
                "name": "Capacity Pressure Index",
                "category": "capacity_intelligence"
            },
            {
                "name": "Forecast Engine",
                "category": "forecasting"
            },
            {
                "name": "Infrastructure Risk Signal",
                "category": "risk_intelligence"
            },
            {
                "name": "Provider Ranking Engine",
                "category": "provider_intelligence"
            },
            {
                "name": "Provider Recommendation Engine",
                "category": "decision_support"
            },
            {
                "name": "Enterprise Decision Engine",
                "category": "executive_intelligence"
            }
        ]
    }
