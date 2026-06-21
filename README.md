# AI-RPCT

**Version:** v66.0  
(see `VERSION.md` for release notes and current status)

AI Resource Pressure & Capacity Tracker.

AI-RPCT is a local AI infrastructure intelligence system that tracks market data, GPU supply indicators, provider rankings, shortage probability, forecast signals, and dashboard reporting.

## Current Features

- Market data collector
- GPU provider collector architecture
- RPCT score engine
- Provider ranking engine
- GPU shortage probability engine
- Forecast signal engine
- Trend engine
- Daily text reports
- Markdown research snapshots
- Local HTML dashboard
- JSON metrics export
- FastAPI service
- Git versioning
- Automated daily pipeline
- Backup script

## Run Pipeline

```bash
./run_daily.sh
open dashboard.html
```

## SQLite Database

Initialize database:

```bash
python database/init_db.py
python database/import_csv.py
python database/db_status.py
./backup_db.sh
data/airpct.db
```

## AI-RPCT Terminal UI Demo

Run the local intelligence terminal:

```bash
./run_ui_demo.sh
```

Then open:

    http://127.0.0.1:8000/web

API dashboard endpoint

The web UI loads aggregated KPI data from the API endpoint `GET /dashboard-metrics` (JSON). You can fetch it directly:

```bash
curl http://127.0.0.1:8000/dashboard-metrics
```
This returns a compact JSON object with keys like `data_moat_score`, `executive_score`, `product_readiness_score`, `collection_health`, and `investor_readiness_score` used by `web/dashboard.html`.

The terminal includes:

- Executive Market Narrative
- Investor / Buyer Snapshot
- Data Moat Panel
- Provider Concentration Alert
- Forecast Readiness
- GPU Market Depth
- GPU Market Leaders
- Daily Alpha Feed
- Market Movers
- System Health Strip
- Provider Demo Mode Warning

## API Key Access

The PDF export and download endpoints are protected via `X-API-KEY`.
Set the allowed keys via environment variable `AI_RPCT_API_KEYS`, e.g.:

```bash
export AI_RPCT_API_KEYS=demo-key
```

For local/demo use the built-in default `demo-key`.

## Docker

Build and run the container with requirements from `requirements.txt`:

```bash
docker build -t ai-rpct .
docker run -p 8000:8000 -e AI_RPCT_API_KEYS=demo-key ai-rpct
```

For production builds, use the `Dockerfile.prod` image:

```bash
docker build -f Dockerfile.prod -t ai-rpct:prod .
docker run -p 8000:8000 -e AI_RPCT_API_KEYS=prod-key ai-rpct:prod
```

A `.dockerignore` file is included to keep build context small and avoid packaging local artifacts.

## Docker Compose

Use the provided `docker-compose.yml` for production-style deployment:

```bash
docker compose -f docker-compose.yml up --build
```

The service exposes health endpoints that Docker uses for container health checks:

- `GET /health` → service status and uptime
- `GET /ready` → readiness status

For local development with live source and data mounting, use the included override file:

```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

A sample `.env.example` is included with `AI_RPCT_API_KEYS=demo-key`.

To override the API keys for non-demo use:

```bash
export AI_RPCT_API_KEYS="prod-key-1,prod-key-2"
docker compose -f docker-compose.yml up --build
```

### Makefile

Use `make` to simplify local development:

```bash
make install
make run
```

Build and run in Docker:

```bash
make docker-build
make docker-up
```

Run compose with local overlay:

```bash
make compose-up
```

Run production-style compose:

```bash
make compose-prod
```

For one-step production deployment, use the new script:

```bash
export AI_RPCT_API_KEYS="prod-key-1,prod-key-2"
./deploy.sh
```

Or use the Make shortcut:

```bash
make deploy
```

The compose setup includes a healthcheck and a default API key fallback for demo mode.

## Release & Versioning

- Current version and release status are tracked in `VERSION.md`.
- Update `VERSION.md` and `RELEASE_NOTES.md` before a new product release.
- Use `git tag` for release versioning and deploy the tagged image.
- Use `make release` to create a tag from `VERSION.md`.

