# AI-RPCT Customer-Ready Executive Brief

Generated: 2026-06-24T14:14:05.281168

## Headline
AI infrastructure stress is watch; signal performance is building.

## Decision
Collect 27 more daily records to reach the 30-day milestone.

## Signal Performance
- Score: 43.09
- Band: building
- Blockers: reach_30_clean_daily_records, increase_source_url_coverage, make_paid_facing_points_paid_safe

## Claim Posture
- Current posture: research_preview
- Allowed claim gates: 1
- Blocked claim gates: 3

## Customer Watchlist
- provider: vast (high) -> Refresh live provider ingestion and verify connector scheduling.
- provider: vast (high) -> Restore fresh live provider ingestion or rotate credentials before relying on the provider score.
- provider: vast (high) -> Collect daily provider metrics until 30 distinct history days are available.
- provider: runpod (high) -> Refresh live provider ingestion and verify connector scheduling.
- provider: runpod (high) -> Restore fresh live provider ingestion or rotate credentials before relying on the provider score.
- provider: runpod (high) -> Collect daily provider metrics until 30 distinct history days are available.
- market_signal: GPU Scarcity Index (watch) -> monitor_daily_scarcity_direction
- price_dislocation: H100 (watch) -> compare_provider_prices_before_buying
- provider: runpod (medium) -> Increase offer coverage or add a second source for this provider.
- snapshot_target: vast / A100 PCIe / eu-central (medium) -> collect_source_labeled_snapshot

## Explainability Drilldown
- gpu_scarcity_index / availability_pressure_score: 44.5 (0.35)
- gpu_scarcity_index / price_pressure_score: 37.73 (0.25)
- gpu_scarcity_index / frontier_pressure_score: 28.66 (0.25)
- gpu_scarcity_index / provider_depth_score: 100.0 (0.15)
- capacity_shock_forecast / latest_rpct: 100.0 (0.4)
- capacity_shock_forecast / shortage_probability: 40.0 (0.25)
- capacity_shock_forecast / gpu_scarcity_index: 34.06 (0.25)
- capacity_shock_forecast / capacity_shock_delta: 0.0 (0.1)

## Source Evidence
- lambda_labs / A100 PCIe / eu-central: linked
- runpod / A100 PCIe / eu-central: linked
- vast / A100 PCIe / eu-central: linked

## Guardrail
This brief is research-preview unless all claim gates are paid-safe.