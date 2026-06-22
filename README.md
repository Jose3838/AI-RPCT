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
- FastAPI service
- SQLite import path
- automated daily pipeline
- beta/readiness dashboards

## Daily Terminal Run

Use the virtual environment directly:

```bash
venv/bin/python -m pytest
./run_daily.sh
venv/bin/python database/db_status.py
```

Start the API locally:

```bash
venv/bin/uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/web
http://127.0.0.1:8000/v1/dashboard-snapshot
```

## Stable V1 API Core

These endpoints are the product surface we should protect first:

- `/v1/terminal-summary`
- `/v1/dashboard-snapshot`
- `/v1/api-catalog`
- `/v1/access-status`
- `/v1/plan-limits`
- `/v1/usage-summary`
- `/v1/commercial-snapshot`
- `/v1/sales-pipeline`
- `/v1/customers`
- `/v1/customers/revoke`
- `/v1/customers/reactivate`
- `/v1/reports/latest`
- `/v1/signals`
- `/v1/recommendations`
- `/v1/executive-brief`
- `/v1/customer-report`
- `/v1/customer-report/html`

## Data Flow

```text
collectors -> data/*.csv -> engine -> analytics -> reports/dashboard/API
```

Core files:

- `collectors/collect_market_data.py`
- `collectors/collect_gpu_data.py`
- `engine/calculate_rpct.py`
- `analytics/*`
- `data/*.csv`
- `main.py`
- `api/routes.py`
- `web/app.js`
- `run_daily.sh`

## MVP Priorities

1. Stabilize the daily data pipeline.
2. Make provider live-data ingestion reliable.
3. Define 3-5 unique intelligence signals.
4. Build a clear terminal dashboard.
5. Add historical data quality checks.
6. Package investor/customer reports.
7. Add API keys, plans, usage limits, and billing readiness.

## Unique Signals To Build

- AI Infrastructure Stress Index
- GPU Scarcity Index
- Provider Reliability Score
- Capacity Shock Forecast
- Price Dislocation Signal
- Enterprise Provider Recommendation

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

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/access-status"

curl -H "x-api-key: demo-pro-key" \
  "http://127.0.0.1:8000/v1/usage-summary"
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
