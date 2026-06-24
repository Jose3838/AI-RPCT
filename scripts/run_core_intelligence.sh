#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."
source venv/bin/activate
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

echo "=============================="
echo "AI-RPCT CORE INTELLIGENCE RUN"
date
echo "=============================="

python analytics/provider_preflight.py
python analytics/live_provider_ingest.py
python analytics/provider_preflight.py
python analytics/gpu_scarcity_index.py
python analytics/forecast_signal.py
python analytics/price_dislocation_signal.py
python analytics/ai_infrastructure_stress_index.py
python analytics/core_intelligence_alerts.py
python analytics/forecast_accuracy.py
python analytics/provider_health.py
python analytics/provider_daily_metrics.py
python analytics/provider_reliability_ranking.py
python analytics/provider_reliability_gaps.py
python analytics/signal_methodology_registry.py
python analytics/bloomberg_execution_roadmap.py
python scripts/manual_snapshot_copy_ready.py
python analytics/manual_snapshot_ingest.py
python analytics/manual_snapshot_quality.py
python analytics/source_url_coverage_metrics.py
python analytics/source_evidence_view.py
python analytics/source_backed_scarcity.py
python analytics/coverage_universe_status.py
python analytics/snapshot_collection_plan.py
python scripts/manual_snapshot_daily_pack.py
python analytics/region_scarcity_heatmap.py
python analytics/core_signal_history.py
python analytics/collection_cadence_audit.py
python analytics/core_history_audit.py
python analytics/core_provenance_audit.py
python analytics/core_signal_quality.py
python analytics/forecast_validation_history.py
python analytics/provider_reliability_live_overlay.py
python analytics/signal_performance_score.py
python analytics/signal_explainability_drilldowns.py
python analytics/customer_watchlists.py
python analytics/core_intelligence_readiness.py
python analytics/paid_beta_gate.py
python analytics/claim_gate_matrix.py
python analytics/paid_data_point_provenance.py
python snapshot_scheduler.py
python analytics/daily_terminal_brief.py
python analytics/morning_brief.py
python analytics/executive_ai_infrastructure_memo.py
python analytics/customer_ready_executive_brief.py
python analytics/research_preview_brief.py
python scripts/core_status.py

echo "CORE INTELLIGENCE DONE"
