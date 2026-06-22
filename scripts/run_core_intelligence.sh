#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."
source venv/bin/activate
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

echo "=============================="
echo "AI-RPCT CORE INTELLIGENCE RUN"
date
echo "=============================="

python analytics/live_provider_ingest.py
python analytics/gpu_scarcity_index.py
python analytics/forecast_signal.py
python analytics/provider_health.py
python analytics/provider_daily_metrics.py
python analytics/provider_reliability_ranking.py
python analytics/provider_reliability_gaps.py
python analytics/core_signal_history.py
python analytics/core_signal_quality.py
python analytics/core_intelligence_readiness.py
python analytics/market_pulse_snapshot.py
python analytics/daily_terminal_brief.py
python analytics/executive_ai_infrastructure_memo.py
python scripts/core_status.py

echo "CORE INTELLIGENCE DONE"
