# AI-RPCT Master Architecture v1

## Mission

AI-RPCT is a Decision Intelligence Platform for AI infrastructure.

Its purpose is to collect, normalize, analyze, forecast, explain, and recommend actions for strategic AI infrastructure decisions.

## Strategic Goal

AI-RPCT aims to become the decision layer for AI infrastructure markets:

- GPU availability
- Provider capacity
- Market pressure
- Scarcity signals
- Forecast signals
- Provider rankings
- Infrastructure risk
- Executive recommendations

## Platform Layers

### 1. Collection Layer

Existing components:

- collectors/
- collectors/providers/
- providers/connectors/
- warehouse/raw_providers/
- warehouse/live_provider_history/
- warehouse/snapshots/

Purpose:

Collect provider, GPU, market, and snapshot data.

### 2. Normalization Layer

Existing components:

- data_layer/
- analytics/build_*_registry.py
- analytics/builders/
- warehouse/historical/
- warehouse/metadata/

Purpose:

Transform raw and historical data into governed registries and normalized datasets.

### 3. Intelligence Layer

Existing components:

- analytics/forecast_signal.py
- analytics/gpu_scarcity_index.py
- analytics/gpu_price_trend_signal.py
- analytics/intelligence_signal_score.py
- analytics/provider_rankings.py
- analytics/provider_health.py
- analytics/market_intelligence_snapshot.py
- analytics/research_snapshot.py

Purpose:

Generate signals, rankings, snapshots, scarcity indicators, and market intelligence.

### 4. Forecast Layer

Existing components:

- analytics/build_feature_store.py
- analytics/build_forecast_dataset.py
- analytics/run_forecast_engine_v1.py
- analytics/build_forecast_explanations.py
- data/forecast_signal.csv
- data/forecast_engine_v1_output.csv
- warehouse/forecast/

Purpose:

Convert signals and features into forecast outputs and explanations.

### 5. Governance Layer

Existing components:

- analytics/build_data_quality_metrics.py
- analytics/build_data_lineage_registry.py
- analytics/build_registry_metadata.py
- analytics/validate_all_registries.py
- reports/data_quality_metrics_v1.md
- reports/dependency_graph.md
- reports/release_report.md

Purpose:

Track quality, lineage, validation, metadata, and release state.

### 6. Analytics Layer

Existing components:

- warehouse/analytics/ai_rpct.duckdb
- analytics/build_duckdb_analytics_layer.py
- analytics/run_analytics_queries.py
- reports/analytics_queries.md
- reports/analytics_dashboard.md

Purpose:

Provide queryable analytics and derived reporting.

### 7. API Layer

Existing components:

- api/main.py
- api/routes.py
- api/metrics.py
- api/auth_routes.py

Purpose:

Expose registries, forecasts, health, providers, and platform data over HTTP.

### 8. Web Console Layer

Existing components:

- web/index.html
- web/pages/
- web/assets/
- analytics/build_web_console.py
- analytics/build_web_dashboard.py

Purpose:

Present AI-RPCT as a usable executive and operational platform.

### 9. Decision Layer

Existing components:

- enterprise_decision_engine.py
- provider_recommendation_engine.py
- executive_intelligence_summary.py
- executive_market_briefing.py
- investor_snapshot.py
- reports/investor_snapshot_20260617.txt
- reports/market_intelligence_snapshot_20260617.txt

Purpose:

Translate market intelligence into business decisions, recommendations, and executive-facing outputs.

## Current Architecture Finding

AI-RPCT contains two generations of development:

### Generation 1: Intelligence Platform

Focused on:

- market data
- GPU provider data
- live provider status
- scarcity
- rankings
- snapshots
- forecast signals
- executive reports

### Generation 2: Enterprise Platform

Focused on:

- registries
- governance
- metadata
- DuckDB
- FastAPI
- Web Console
- tests
- pipeline orchestration

## CTO Decision

The project should not continue as isolated scripts.

AI-RPCT should be unified into one platform:

```text
Collection
    ↓
Normalization
    ↓
Intelligence
    ↓
Forecast
    ↓
Governance
    ↓
Decision Layer
    ↓
API + Web Console
