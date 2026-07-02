# AI-RPCT Intelligence Architecture v1.0

## Purpose

AI-RPCT is evolving from a collection of analytics modules into a unified Decision Intelligence Platform for AI Infrastructure.

The goal is not to show isolated data, but to transform historical, market, pricing, forecast, risk, and capacity signals into actionable recommendations.

## Intelligence Flow

Raw Data
→ Analytics
→ Knowledge
→ Signals
→ Decision Intelligence
→ Executive Recommendation
→ Action

## Domains

### 1. Historical Intelligence

Purpose:
Understand long-term market behavior, vendor cycles, pricing history, and technology evolution.

Current modules:
- analytics/build_amd_historical_gpu_registry.py
- analytics/build_intel_historical_gpu_registry.py
- analytics/build_nvidia_historical_gpu_registry.py
- analytics/build_historical_pricing_registry.py
- analytics/historical_trends.py
- analytics/history_summary.py
- copilot/historical/service.py

### 2. Pricing Intelligence

Purpose:
Track GPU prices, volatility, price trends, and buying opportunities.

Current modules:
- analytics/gpu_price_trend_signal.py
- analytics/gpu_price_volatility.py
- analytics/live_gpu_price_history.py
- analytics/live_gpu_price_index.py
- analytics/pricing_tiers.py

### 3. Market Intelligence

Purpose:
Understand market movement, vendor dominance, market regimes, and provider shifts.

Current modules:
- analytics/gpu_market_brief.py
- analytics/gpu_market_movers.py
- analytics/market_regime.py
- analytics/market_intelligence_snapshot.py
- analytics/frontier_gpu_index.py
- analytics/provider_marketshare.py
- analytics/provider_dominance_index.py

### 4. Forecast Intelligence

Purpose:
Predict future demand, pricing, risk, and infrastructure needs.

Current modules:
- analytics/forecasting_engine.py
- analytics/forecast_signal.py
- analytics/forecast_accuracy.py
- analytics/run_forecast_engine_v1.py
- analytics/time_series_forecast.py
- copilot/forecast_intelligence.py

### 5. Capacity Intelligence

Purpose:
Analyze available capacity, shortages, infrastructure pressure, and future needs.

Current modules:
- analytics/build_historical_capacity_registry.py
- analytics/shortage_probability.py
- analytics/scarcity_watchlist.py
- analytics/gpu_scarcity_index.py
- copilot/capacity_intelligence.py

### 6. Risk Intelligence

Purpose:
Translate market, provider, pricing, and capacity risks into actionable risk signals.

Current modules:
- analytics/terminal_risk_score.py
- analytics/provider_concentration.py
- analytics/provider_health.py
- analytics/trust_status.py
- copilot/risk_intelligence.py

### 7. Executive Intelligence

Purpose:
Summarize decisions, risks, opportunities, trends, and actions for leadership.

Current modules:
- analytics/build_executive_morning_brief.py
- analytics/executive_dashboard.py
- analytics/executive_ai_infrastructure_memo.py
- copilot/executive/
- copilot/executive/facade.py
- copilot/executive/facade_builder.py

### 8. Decision Intelligence

Purpose:
Fuse all intelligence domains into recommendations.

Current modules:
- analytics/build_decision_summary.py
- analytics/build_decision_explanations.py
- analytics/save_decision_history.py
- copilot/decision.py
- copilot/decision_intelligence.py
- copilot/recommendation.py

## Target Architecture

analytics/
→ domain analytics modules

copilot/
→ service layer

copilot/historical/
→ historical intelligence service

copilot/executive/
→ executive facade and cockpit services

future:
copilot/intelligence/
→ unified intelligence orchestration layer

## Future Unified Intelligence Layer

Planned structure:

copilot/intelligence/
- historical.py
- pricing.py
- market.py
- forecast.py
- capacity.py
- risk.py
- decision.py
- engine.py

## Decision Intelligence Goal

AI-RPCT should answer:

- Should we buy now or wait?
- How many GPUs should we procure?
- Which vendor is strategically best?
- Is cloud or on-prem more economical?
- What is the expected ROI?
- What are the main risks?
- What action should leadership take today?

## Rule

No new intelligence module should be added without first checking whether an existing module can be reused, extended, or composed.
