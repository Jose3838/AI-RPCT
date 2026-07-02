# AI-RPCT Intelligence Inventory v1.0

## Purpose

This document maps existing AI-RPCT analytics and copilot modules to intelligence domains.

The goal is to avoid duplicate development and make future Decision Intelligence work composable.

## Domains

### Historical Intelligence

Modules:
- analytics/build_amd_historical_gpu_registry.py
- analytics/build_intel_historical_gpu_registry.py
- analytics/build_nvidia_historical_gpu_registry.py
- analytics/build_historical_pricing_registry.py
- analytics/build_historical_capacity_registry.py
- analytics/historical_trends.py
- analytics/history_summary.py
- analytics/historical_data_quality.py
- copilot/historical/service.py

Reuse target:
- Historical Intelligence API
- Historical Decision Analytics
- Unified Decision State Engine

### Pricing Intelligence

Modules:
- analytics/gpu_price_trend_signal.py
- analytics/gpu_price_volatility.py
- analytics/live_gpu_price_history.py
- analytics/live_gpu_price_index.py
- analytics/pricing_tiers.py

Reuse target:
- Buy vs Wait Advisor
- ROI Advisor
- Procurement Intelligence

### Market Intelligence

Modules:
- analytics/gpu_market_brief.py
- analytics/gpu_market_movers.py
- analytics/market_regime.py
- analytics/market_intelligence_snapshot.py
- analytics/frontier_gpu_index.py

Reuse target:
- Market Regime Detection
- Vendor Advisor
- Executive Briefing

### Forecast Intelligence

Modules:
- analytics/forecasting_engine.py
- analytics/forecast_signal.py
- analytics/forecast_accuracy.py
- analytics/run_forecast_engine_v1.py
- analytics/time_series_forecast.py
- copilot/forecast_intelligence.py

Reuse target:
- Capacity Advisor
- Procurement Advisor
- Investment Timing

### Capacity Intelligence

Modules:
- analytics/scarcity_watchlist.py
- analytics/shortage_probability.py
- analytics/gpu_scarcity_index.py
- copilot/capacity_intelligence.py

Reuse target:
- Capacity Planning
- Supply Risk
- Infrastructure Scaling

### Risk Intelligence

Modules:
- analytics/terminal_risk_score.py
- analytics/provider_concentration.py
- analytics/provider_health.py
- analytics/trust_status.py
- copilot/risk_intelligence.py

Reuse target:
- Executive Risk
- Procurement Risk
- Vendor Risk

### Executive Intelligence

Modules:
- analytics/build_executive_morning_brief.py
- analytics/executive_dashboard.py
- analytics/executive_ai_infrastructure_memo.py
- copilot/executive/facade.py
- copilot/executive/facade_builder.py

Reuse target:
- Executive Cockpit
- Morning Brief
- Board-Level Reports

### Decision Intelligence

Modules:
- analytics/build_decision_summary.py
- analytics/build_decision_explanations.py
- analytics/save_decision_history.py
- copilot/decision.py
- copilot/decision_intelligence.py
- copilot/recommendation.py

Reuse target:
- Recommendation Engine
- Explainability
- Action Center

## Rule

Before creating a new intelligence module, check this inventory first.

Prefer:
1. Reuse existing module.
2. Extend existing module.
3. Compose existing modules.
4. Create new module only if necessary.
