#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=============================="
echo "AI-RPCT MASTER DAILY CYCLE"
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "=============================="

if [ -d "venv" ]; then
  source venv/bin/activate
fi

python master_daily_cycle_runner.py

echo ""
echo "Daily intelligence cycle completed successfully"
echo ""
