#!/bin/bash
set -euo pipefail

cd /Users/yusufyavuzyasar/AI-RPCT
source venv/bin/activate

mkdir -p logs

{
  echo "HOURLY COLLECTION START $(date -u)"
  python live_data_snapshot_auditor.py
  python live_data_audit_history.py
  python analytics/provider_preflight.py
  python analytics/historical_moat_audit.py
  echo "HOURLY COLLECTION DONE $(date -u)"
} >> logs/hourly_collection.launchd.out.log 2>> logs/hourly_collection.launchd.err.log
