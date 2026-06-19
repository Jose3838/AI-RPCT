# AI-RPCT

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

## SQLite Database

Initialize database:

```bash
python database/init_db.py
python database/import_csv.py
python database/db_status.py
./backup_db.sh
data/airpct.db


## AI-RPCT Terminal UI Demo

Run the local intelligence terminal:

```bash
./run_ui_demo.sh

## AI-RPCT Terminal UI Demo

Run the local intelligence terminal:

```bash
./run_ui_demo.sh

## AI-RPCT Terminal UI Demo

Run the local intelligence terminal:

    ./run_ui_demo.sh

Then open:

    http://127.0.0.1:8000/web

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

