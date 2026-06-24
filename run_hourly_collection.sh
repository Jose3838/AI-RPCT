#!/bin/bash
set -e

cd /Users/yusufyavuzyasar/AI-RPCT
source venv/bin/activate

python live_data_snapshot_auditor.py
python live_data_audit_history.py
python analytics/provider_preflight.py
python analytics/historical_moat_audit.py
