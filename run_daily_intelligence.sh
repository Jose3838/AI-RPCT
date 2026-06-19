#!/bin/bash

cd "$(dirname "$0")"

if [ -d "venv" ]; then
  source venv/bin/activate
fi

python master_daily_cycle_runner.py

echo ""
echo "Daily intelligence cycle completed"
echo ""
