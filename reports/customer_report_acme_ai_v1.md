# AI-RPCT Customer Intelligence Report

Customer: Acme AI
Generated: 2026-06-21T17:23:48.886360+00:00

## Executive Summary
AI infrastructure risk remains elevated.

The terminal is showing elevated infrastructure risk, with frontier GPU scarcity and provider concentration requiring active monitoring.

## Core Metrics
- AI Infrastructure Index: 75.6
- GPU Price Index: 4.1204
- GPU Price Trend: stable
- Terminal Risk Score: 75
- Risk Level: high
- Top Provider: vast
- Live Data Quality Score: 100.0

## Decision Signals
### Risk is in watch mode
- Type: risk
- Severity: medium
- Message: The market is not calm, but current conditions do not require immediate escalation.
- Evidence: terminal_risk_score: 75.0

### GPU pricing is stable
- Type: market
- Severity: low
- Message: Pricing is not showing a strong directional move in the latest observation window.
- Evidence: gpu_price_trend: stable | change_pct: 0.0

### Cheapest tracked GPU: Tesla V100
- Type: buying_signal
- Severity: low
- Message: This GPU currently offers the lowest average tracked price.
- Evidence: gpu: Tesla V100 | avg_price: 0.0401 | min_price: 0.0209 | offers: 5

### Most expensive tracked GPU: B200
- Type: premium_pressure
- Severity: medium
- Message: High average pricing here can indicate frontier demand pressure or limited supply.
- Evidence: gpu: B200 | avg_price: 15.418 | max_price: 40.0069 | offers: 11

### Frontier GPU scarcity detected
- Type: scarcity
- Severity: high
- Message: One or more frontier GPUs are flagged as scarce and should be watched closely.
- Evidence: gpus: B300, H100 SXM | count: 2

## Recommended Actions
### Use vast as the primary provider benchmark
- Action: primary_provider_watch
- Priority: medium
- Rationale: This provider has the strongest current combination of online status and tracked offer depth.
- Evidence: provider: vast | offers: 100 | gpu_types: 21 | avg_price: 4.1204

### Track low-cost capacity around Tesla V100
- Action: track_low_cost_capacity
- Priority: medium
- Rationale: This is currently the lowest-cost tracked GPU and can anchor budget-sensitive workloads.
- Evidence: gpu: Tesla V100 | avg_price: 0.0401 | min_price: 0.0209 | offers: 5

### Protect frontier GPU capacity decisions
- Action: protect_frontier_capacity
- Priority: high
- Rationale: Frontier GPU scarcity is visible. Avoid relying on a single provider or a single GPU type.
- Evidence: scarce_gpus: B300, H100 SXM | count: 2

### Maintain watch mode
- Action: maintain_watch_mode
- Priority: medium
- Rationale: Risk is elevated but not extreme. Keep monitoring before making irreversible commitments.
- Evidence: terminal_risk_score: 75.0

## Notes
This report is generated from AI-RPCT terminal data. Provider API keys and live-data freshness should be reviewed before using this report for contractual purchase decisions.