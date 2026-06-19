#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "======================================"
echo " AI-RPCT UI DEMO START"
echo "======================================"

if [ -d "venv" ]; then
  source venv/bin/activate
fi

echo "Running UI smoke test..."
python ui_smoke_test.py

echo "Running UI file check..."
python ui_file_check.py

echo "Checking data assets..."
ls -lh data/live_offers || true
ls -lh data/feature_store || true

echo "Starting FastAPI..."
echo "Open: http://127.0.0.1:8000/web"

uvicorn main:app --reload
