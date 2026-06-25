#!/bin/bash
set -euo pipefail

cd /Users/yusufyavuzyasar/AI-RPCT
source venv/bin/activate

mkdir -p logs

{
  echo "DAILY COLLECTION START $(date -u)"
  python analytics/free_source_audit.py
  python analytics/historical_moat_audit.py
  python analytics/live_provider_ingestion_runner.py
  python analytics/provider_history_writer.py
  python analytics/provider_preflight.py
  python live_data_snapshot_auditor.py
  python live_data_audit_history.py
  echo "DAILY COLLECTION DONE $(date -u)"
} >> logs/launchd.daily.out.log 2>> logs/launchd.daily.err.log

# AI-RPCT forecast lifecycle governance
python analytics/forecast_lifecycle_orchestrator_v1.py
python analytics/auto_retraining_manager_v1.py
python analytics/production_promotion_guard_v1.py
python analytics/ai_rpct_readiness_dashboard_v1.py
