#!/bin/bash
set -euo pipefail

cd /Users/yusufyavuzyasar/AI-RPCT
source venv/bin/activate

mkdir -p logs

{
  echo "DAILY COLLECTION START $(date -u)"
  python analytics/free_source_audit.py
  python analytics/historical_moat_audit.py
  python analytics/provider_preflight.py
  python live_data_snapshot_auditor.py
  python live_data_audit_history.py
  echo "DAILY COLLECTION DONE $(date -u)"
} >> logs/launchd.daily.out.log 2>> logs/launchd.daily.err.log
