# AI-RPCT Platform Layers

## Layer 1 — Collection

Purpose

Collect raw provider, GPU, cloud, pricing and market data.

Current Modules

- collectors/
- providers/connectors/
- warehouse/raw_providers/
- warehouse/live_provider_history/
- warehouse/snapshots/

Status

Existing
Needs consolidation.

------------------------------------------------

## Layer 2 — Registry

Purpose

Normalize infrastructure entities.

Examples

- Historical Registry
- Provider Registry
- Accelerator Registry
- Software Registry

Status

Strong

------------------------------------------------

## Layer 3 — Intelligence

Purpose

Transform raw information into market intelligence.

Examples

- GPU Scarcity
- Provider Rankings
- Market Signals
- Trend Engine
- Executive Snapshots

Status

Large but fragmented.

------------------------------------------------

## Layer 4 — Forecast

Purpose

Predict future market conditions.

Examples

- Forecast Dataset
- Forecast Engine
- Forecast Explanations
- Feature Store

Status

Strong

------------------------------------------------

## Layer 5 — Decision Intelligence

Purpose

Turn intelligence into business recommendations.

Future Examples

- Buy Recommendation
- Capacity Reservation
- Provider Switching
- Budget Planning
- Strategic Risk

Status

Beginning

------------------------------------------------

## Layer 6 — Platform

Purpose

Expose everything.

Includes

- API
- DuckDB
- Web Console
- Dashboard
- Reports
- Tests

Status

Strong
