#!/bin/bash
cd /app 2>/dev/null || cd ~/AI-RPCT
export PYTHONPATH="$PWD"

python database/init_db.py || true
python database/import_csv.py || true
python analytics/live_provider_market_share.py || true

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
