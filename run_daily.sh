#!/bin/bash
cd ~/AI-RPCT
source venv/bin/activate

echo "=============================="
echo "AI-RPCT DAILY RUN"
echo "$(date)"
echo "=============================="

python collectors/collect_market_data.py
python collectors/collect_gpu_data.py
python engine/calculate_rpct.py

python analytics/provider_rankings.py
python analytics/provider_health.py
python analytics/provider_marketshare.py
python analytics/provider_concentration.py
python analytics/provider_credentials.py
python analytics/provider_readiness.py
python analytics/shortage_probability.py
python analytics/forecast_signal.py
python analytics/trend_engine.py
python analytics/time_series_forecast.py
python analytics/market_regime.py
python analytics/predictor.py
python analytics/investor_metrics.py
python analytics/investor_dashboard.py
python analytics/executive_dashboard.py
python analytics/backtest.py
python analytics/forecast_accuracy.py
python analytics/provider_history.py
python analytics/alert_engine.py
python analytics/data_quality.py
python analytics/production_readiness.py
python analytics/operational_status.py
python analytics/data_validator.py

python api/metrics.py
python database/init_db.py
python database/import_csv.py
python analytics/daily_report.py
python analytics/research_snapshot.py
python dashboard/dashboard.py

echo "DONE"
python analytics/ai_infrastructure_index.py
python analytics/gpu_scarcity_index.py
python analytics/index_history.py
python analytics/archive_daily_snapshot.py
python analytics/provider_daily_metrics.py
python analytics/provider_dominance_index.py
python analytics/cron_health.py
python analytics/data_moat_score.py
python analytics/daily_intelligence_summary.py
python analytics/archive_raw_provider_data.py
python analytics/data_freshness.py
python analytics/live_provider_status.py
python analytics/provider_data_mode.py
python analytics/public_beta_status.py
python analytics/commercial_readiness.py
python analytics/launch_readiness.py
python analytics/live_provider_ingest.py
python analytics/archive_live_provider_data.py
python analytics/live_gpu_price_index.py
python analytics/live_gpu_price_history.py
python analytics/live_offer_summary.py
python analytics/live_gpu_rankings.py
python analytics/gpu_market_movers.py
python analytics/live_gpu_alerts.py
