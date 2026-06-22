# Core Intelligence Focus

AI-RPCT is being built as an AI infrastructure intelligence product, not as a collection of dashboards, APIs, or provider directories.

The Bloomberg-style goal is simple:

> A serious user should have a reason to open AI-RPCT every morning before making AI infrastructure decisions.

## Product Doctrine

- The raw data is not the moat.
- The historical signal time series is the moat.
- Cost discipline stays in place until customers prove the signal is valuable.
- New APIs are frozen unless they directly strengthen core intelligence, data quality, historical collection, or paid-customer validation.
- Commercial and operations features are supporting infrastructure, not the product center.

## Core Intelligence Surface

These endpoints are the product surface to protect and improve first:

- `/v1/dashboard-snapshot`
- `/v1/market-pulse`
- `/v1/signals`
- `/v1/recommendations`
- `/v1/executive-brief`

The user-facing question for every core endpoint is:

> Does this help a buyer, builder, investor, or infrastructure team understand what changed in the AI infrastructure market and what to do next?

## 30-Day Priorities

1. Daily pipeline reliability
2. Historical time-series completeness
3. GPU Scarcity Index
4. Capacity Shock Forecast
5. Provider Reliability Score
6. First paying user

Do not add new dashboards during this phase unless they expose one of the three priority signals more clearly.

## Signal Priorities

### GPU Scarcity Index

Purpose: show whether GPU capacity is becoming easier or harder to obtain.

Inputs to strengthen:

- provider availability
- instance inventory
- price movement
- delivery or lead-time signals
- regional concentration

### Capacity Shock Forecast

Purpose: warn when the market is moving toward a capacity squeeze or sudden relief.

Inputs to strengthen:

- day-over-day and week-over-week signal movement
- provider outages
- fast price changes
- repeated availability degradation
- confidence based on data freshness and provider coverage

### Provider Reliability Score

Purpose: help users compare which providers can be trusted for production planning.

Inputs to strengthen:

- live connector health
- provider status history
- data freshness
- price stability
- availability consistency

## Operating Metrics

Track these before adding more product surface:

- days of clean history collected
- provider coverage count
- stale-source count
- daily pipeline success rate
- signal confidence
- number of user interviews
- number of paid beta commitments

## Definition Of Done For Paid Beta

AI-RPCT is ready to charge the first customer when:

- the daily pipeline runs reliably for 30 consecutive days
- the Core Intelligence endpoints are stable
- the product clearly labels confidence and data gaps
- one target user says the daily brief would change a real workflow
- billing and terms are ready enough for a small paid beta

