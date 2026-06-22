# Live Provider Recovery Runbook

AI-RPCT should not make paid provider reliability claims while the core readiness phase is `blocked_by_live_data`.

## Current Blocker Meaning

- `restore_live_provider_ingestion`: live provider connectors are using fallback data.
- `refresh_provider_connectors`: provider timestamps are stale or expired.
- `improve_provider_reliability_depth`: provider reliability score is below the minimum useful threshold.
- `collect_30_days_of_core_signal_history`: the signal moat is still too young for strong paid claims.

## Daily Check

Run:

```bash
./scripts/run_core_intelligence.sh
venv/bin/python scripts/core_status.py
```

Then inspect:

- `data/live_provider_ingestion_status.csv`
- `data/provider_reliability_gaps.csv`
- `data/core_signal_quality.csv`
- `data/core_intelligence_readiness.csv`
- `reports/daily_terminal_brief_YYYYMMDD.txt`

`scripts/core_status.py` prints the current readiness phase, blockers, next action and a prioritized action plan.

## Recovery Order

1. Configure valid `VAST_API_KEY` and `RUNPOD_API_KEY`.
2. Run `./scripts/run_core_intelligence.sh`.
3. Confirm `scripts/core_status.py` no longer lists critical provider-preflight actions.
4. Confirm `live_provider_ingestion_status.csv` shows `fresh`, not `fallback`.
5. Confirm `provider_reliability_gaps.csv` no longer contains `provider_ingestion_using_fallback`.
6. Run the core pipeline daily until 30 distinct signal-history days are collected.
7. Only sell paid reliability claims once `core_intelligence_readiness.csv` leaves `blocked_by_live_data`.

## Priority Order

Follow `action_plan` from `scripts/core_status.py` in this order:

1. Critical provider-preflight actions
2. High-priority provider reliability gaps
3. Core signal history collection
4. Remaining medium/low provider coverage work

## Paid Beta Rule

Paid beta can begin only when:

- core readiness phase is not `blocked_by_live_data`
- no high-priority fallback ingestion gaps remain
- core signal history has 30 clean days
- executive brief clearly labels remaining confidence limits
