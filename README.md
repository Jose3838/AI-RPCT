# AI-RPCT

AI Resource Pressure & Capacity Tracker.

AI-RPCT is an AI infrastructure intelligence system for tracking GPU supply, provider health, pricing pressure, market stress, forecast signals, and executive-ready reports.

The long-term goal is to become a Bloomberg-style intelligence terminal for AI infrastructure: live market data, trusted historical signals, provider comparisons, risk alerts, and decision support for builders, buyers, investors, and infrastructure teams.

## CTO Strategy

Build the cheapest useful version first.

Do not spend aggressively on infrastructure before the signal is valuable. The current plan is:

- develop locally
- use CSV and SQLite while the product is still early
- use existing provider APIs where possible
- run the daily pipeline manually or with a lightweight cron
- deploy only the API/dashboard needed for beta users
- add paid infrastructure only after real users validate the value

The product direction is now deliberately narrower:

- AI-RPCT is an intelligence product, not a generic GPU marketplace.
- The moat is the historical signal time series, not the raw data alone.
- API expansion is frozen unless a new endpoint directly improves core intelligence, data quality, historical collection, or customer validation.
- Commercial and operations endpoints support the product, but they are not the product core.

## Current System

- market data collector
- GPU provider collector architecture
- RPCT score engine
- provider ranking engine
- GPU shortage probability engine
- forecast signal engine
- trend engine
- daily text reports
- markdown research snapshots
- local HTML dashboard
- web terminal with market pulse, paid intelligence unlocks, and commercial panels
- FastAPI service
- SQLite import path
- automated daily pipeline
- beta/readiness dashboards

## Daily Terminal Run

Use the virtual environment directly:

```bash
PYTHONPATH=. venv/bin/pytest tests
./run_daily.sh
./scripts/run_core_intelligence.sh
venv/bin/python scripts/core_status.py
venv/bin/python scripts/provider_env_check.py
venv/bin/python scripts/provider_recovery_plan.py
venv/bin/python scripts/scheduler_health.py
venv/bin/python scripts/secret_hygiene_check.py
venv/bin/python analytics/collection_cadence_audit.py
venv/bin/python analytics/signal_methodology_registry.py
venv/bin/python analytics/bloomberg_execution_roadmap.py
venv/bin/python analytics/price_dislocation_signal.py
venv/bin/python analytics/morning_brief.py
venv/bin/python scripts/history_backfill_plan.py
venv/bin/python scripts/manual_snapshot_workflow.py
venv/bin/python scripts/founder_daily_close.py
venv/bin/python scripts/manual_snapshot_inbox_template.py
venv/bin/python scripts/manual_snapshot_template_check.py
venv/bin/python scripts/manual_snapshot_copy_ready.py
venv/bin/python analytics/manual_snapshot_ingest.py
venv/bin/python analytics/paid_beta_gate.py
venv/bin/python snapshot_scheduler.py
venv/bin/python database/db_status.py
```

Install the free macOS auto-runner:

```bash
./scripts/install_macos_launch_agent.sh
./scripts/macos_launch_agent_status.sh
./scripts/uninstall_macos_launch_agent.sh
```

The LaunchAgent runs `./scripts/run_core_intelligence.sh` at login and every day at 08:15 local time while the Mac is awake. Logs are written to `logs/launchd.daily.out.log` and `logs/launchd.daily.err.log`.

The morning brief writes both a markdown report in `reports/` and a structured summary at `data/morning_brief_summary.csv`.

Start the API locally:

```bash
venv/bin/uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/web
http://127.0.0.1:8000/v1/dashboard-snapshot
http://127.0.0.1:8000/v1/market-pulse
```

## Stable V1 API Surface

These endpoints are the Core Intelligence surface we should protect first:

- `/v1/dashboard-snapshot`
- `/v1/market-pulse`
- `/v1/signals`
- `/v1/recommendations`
- `/v1/executive-brief`

Supporting commercial and operations endpoints exist for customer validation, access control, reporting, and launch readiness. They should stay stable, but new work should not expand that surface until the Core Intelligence layer is stronger.

See `docs/CORE_INTELLIGENCE_FOCUS.md` for the current CTO execution doctrine.

## Data Flow

```text
collectors -> data/*.csv -> engine -> analytics -> reports/dashboard/API
```

Core files:

- `collectors/collect_market_data.py`
- `collectors/collect_gpu_data.py`
- `engine/calculate_rpct.py`
- `analytics/*`
- `analytics/market_pulse_snapshot.py`
- `analytics/morning_brief.py`
- `analytics/signal_methodology_registry.py`
- `analytics/bloomberg_execution_roadmap.py`
- `analytics/price_dislocation_signal.py`
- `analytics/core_signal_history.py`
- `analytics/collection_cadence_audit.py`
- `analytics/core_signal_quality.py`
- `analytics/core_intelligence_readiness.py`
- `analytics/paid_beta_gate.py`
- `analytics/core_provenance_audit.py`
- `analytics/coverage_universe_status.py`
- `analytics/manual_snapshot_ingest.py`
- `analytics/manual_snapshot_quality.py`
- `analytics/research_preview_brief.py`
- `analytics/snapshot_collection_plan.py`
- `analytics/provider_preflight.py`
- `analytics/provider_reliability_gaps.py`
- `data/*.csv`
- `data/gpu_universe.csv`
- `data/provider_universe.csv`
- `data/region_universe.csv`
- `data/manual_market_snapshots.csv`
- `data/manual_market_snapshot_inbox.csv`
- `data/launch_controls.csv`
- `main.py`
- `api/routes.py`
- `web/app.js`
- `run_daily.sh`
- `scripts/run_core_intelligence.sh`
- `scripts/core_status.py`
- `scripts/founder_daily_close.py`
- `scripts/manual_snapshot_inbox_template.py`
- `scripts/manual_snapshot_template_check.py`
- `scripts/manual_snapshot_copy_ready.py`
- `scripts/manual_snapshot_workflow.py`
- `scripts/install_macos_launch_agent.sh`
- `scripts/macos_launch_agent_status.sh`
- `scripts/scheduler_health.py`
- `scripts/uninstall_macos_launch_agent.sh`
- `scripts/provider_recovery_plan.py`
- `scripts/history_backfill_plan.py`

Operational runbooks:

- `docs/LIVE_PROVIDER_RECOVERY_RUNBOOK.md`

Current core status:

```bash
venv/bin/python scripts/core_status.py
```

The status output includes readiness phase, paid-beta signal readiness, paid-beta gate status, blockers, next action, and a prioritized action plan.

## MVP Priorities

1. Stabilize the daily data pipeline.
2. Build complete historical time series.
3. Make provider live-data ingestion reliable.
4. Improve GPU Scarcity Index.
5. Improve Capacity Shock Forecast.
6. Improve Provider Reliability Score.
7. Validate the product with the first paying user.

## Unique Signals To Build

- AI Infrastructure Stress Index
- GPU Scarcity Index
- Provider Reliability Score
- Capacity Shock Forecast
- Price Dislocation Signal
- Enterprise Provider Recommendation

The public data trust status is exposed at `/v1/data-trust-status`.
The trust remediation plan is exposed at `/v1/trust-remediation-plan`.
The provider connector readiness matrix is exposed at `/v1/provider-connector-readiness`.
The provider connector upgrade workflow is exposed at `/v1/provider-connector-upgrade-plan`.
The first proprietary market pulse is exposed at `/v1/market-pulse`.
The market pulse history is exposed at `/v1/market-pulse-history` and requires a Pro or Enterprise API key.
The market pulse brief is exposed at `/v1/market-pulse-brief` and requires a Pro or Enterprise API key.
The provider risk radar is exposed at `/v1/provider-risk-radar` and requires a Pro or Enterprise API key.
The daily change brief is exposed at `/v1/daily-change-brief` and requires a Pro or Enterprise API key.
The first decision-signal layer is exposed at `/v1/signals` and included in `/v1/dashboard-snapshot`.
The first recommendation layer is exposed at `/v1/recommendations` and requires a Pro or Enterprise API key.
The first executive brief is exposed at `/v1/executive-brief` and requires a Pro or Enterprise API key.
The first PDF-ready customer report is exposed at `/v1/customer-report` and `/v1/customer-report/html`.

## Cost Discipline

Expected early costs should stay close to zero:

- local development: free
- GitHub: free
- SQLite: free
- provider API keys: usually free to start
- hosting: defer or keep to a small Railway/Fly/Render instance
- domain: optional until beta

The product should earn its right to more infrastructure.

## Demo API Keys

Local demo keys are stored in `data/api_key_registry.csv`:

- `demo-free-key`
- `demo-pro-key`
- `demo-enterprise-key`

Enterprise customer reports require the enterprise key:

```bash
curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/customer-report/html?customer_name=Acme%20AI"
```

Access and usage checks:

```bash
curl "http://127.0.0.1:8000/v1/plan-limits"

curl "http://127.0.0.1:8000/v1/data-trust-status"

curl "http://127.0.0.1:8000/v1/trust-remediation-plan"

curl "http://127.0.0.1:8000/v1/provider-connector-readiness"

curl "http://127.0.0.1:8000/v1/provider-connector-upgrade-plan"

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/access-status"

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/usage-summary"

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/market-pulse-history"

curl -X POST -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/market-pulse/snapshot"

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/market-pulse-brief"

curl -X POST -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/market-pulse-brief/save"

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/provider-risk-radar"

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/daily-change-brief"
```

Plan limits are enforced on authenticated V1 endpoints:

- Free: 50 requests/day, 1,000 requests/month
- Pro: 10,000 requests/day, 250,000 requests/month
- Enterprise: 1,000,000 requests/day, 10,000,000 requests/month

Enterprise commercial snapshot:

```bash
curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/commercial-snapshot"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/sales-pipeline"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/customer-admin"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/account-health"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/revenue-forecast"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/commercial-board-report/html"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/audit-log"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/operations-status"

curl -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/launch-controls"

curl -X POST -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/customers?customer_name=Acme%20AI&plan=pro"

curl -X POST -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/customers/revoke?api_key=airpct_customer_key"

curl -X POST -H "x-api-key: demo-enterprise-key" \
  "http://127.0.0.1:8000/v1/customers/reactivate?api_key=airpct_customer_key"
```

## Current Caveats

- Real provider API keys are not configured yet.
- Some live provider data uses last-known-good fallback data.
- The `intelligence/` source tree appears incomplete in the current checkout.
- The API surface has grown quickly and needs consolidation.
- Many analytics outputs are CSV-based and should later move into a stronger database model.

## North Star

AI-RPCT should become the operating terminal for AI infrastructure markets: trusted, fast, explainable, and valuable enough that customers check it before buying GPU capacity, choosing a provider, or making infrastructure investment decisions.
