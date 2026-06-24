#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
source venv/bin/activate
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

echo "=============================="
echo "AI-RPCT HOURLY COLLECTION"
date -u +"%Y-%m-%dT%H:%M:%SZ"
echo "=============================="

python scheduled_runner_v2.py

echo
echo "Hourly collection completed successfully"
