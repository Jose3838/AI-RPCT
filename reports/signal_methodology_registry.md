# AI-RPCT Signal Methodology Registry

Every core signal must be explainable, source-aware and gated before paid claims.

## GPU Scarcity Index
- Signal ID: gpu_scarcity_index
- Role: Measures current supply pressure across price, availability, frontier GPU stress and provider depth.
- Inputs: data/gpu_data.csv
- Formula: 0.35 availability pressure + 0.30 price pressure + 0.25 frontier pressure + 0.10 provider depth pressure
- Output: data/gpu_scarcity_index.csv -> gpu_scarcity_index
- Trust Gate: Requires fresh provider data and source-labeled manual snapshots before paid market claims.
- Moat Value: Daily scarcity history becomes harder to copy as source-backed observations accumulate.
- Claim Scope: research_preview
- Paid-Safe Requirement: 30+ clean daily history records, no fallback contamination and enough source-labeled region/provider snapshots.

## Capacity Shock Forecast
- Signal ID: capacity_shock_forecast
- Role: Estimates forward-looking infrastructure pressure using RPCT trend, shortage probability, scarcity and shock delta.
- Inputs: data/rpct_scores.csv|data/shortage_probability.csv|data/gpu_scarcity_index.csv
- Formula: 0.40 latest RPCT + 0.25 shortage probability + 0.25 scarcity + 0.10 shock pressure
- Output: data/forecast_signal.csv -> forecast_score
- Trust Gate: Requires forecast validation history before customer-facing predictive claims.
- Moat Value: Forecast usefulness compounds when predictions can be compared against future observed pressure.
- Claim Scope: research_preview
- Paid-Safe Requirement: Measured forecast accuracy, 30+ history days and no unsupported prediction language.

## Provider Reliability Score
- Signal ID: provider_reliability_score
- Role: Ranks providers by health, freshness, data depth, availability, price stability, history and rank score.
- Inputs: data/provider_health.csv|data/provider_daily_metrics.csv
- Formula: 0.25 health + 0.20 freshness + 0.10 depth + 0.10 availability + 0.10 price stability + 0.15 history + 0.10 rank
- Output: data/provider_reliability_ranking.csv -> reliability_score
- Trust Gate: Requires live provider ingestion or explicit fallback disclosure.
- Moat Value: Provider behavior history and fallback/provenance labels create trust that a cloned table lacks.
- Claim Scope: research_preview
- Paid-Safe Requirement: Live provider ingestion green, 30+ provider history days and no missing critical credentials.

## Price Dislocation Signal
- Signal ID: price_dislocation_signal
- Role: Detects unusually wide cross-provider price spreads for the same GPU.
- Inputs: data/gpu_data.csv
- Formula: For GPUs with 2+ provider prices, max spread pct = (max price - min price) / median price; score is capped at 100.
- Output: data/price_dislocation_signal.csv -> price_dislocation_score
- Trust Gate: Requires source-labeled price observations and persistence checks before paid claims.
- Moat Value: Daily spread history can reveal recurring provider mispricing that static price tables miss.
- Claim Scope: research_preview
- Paid-Safe Requirement: Source-backed cross-provider observations, 30+ days of spread history and validated recurrence.