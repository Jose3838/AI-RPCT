#!/bin/bash
cd ~/AI-RPCT
source venv/bin/activate

python collectors/collect_market_data.py
python collectors/collect_gpu_data.py
python engine/calculate_rpct.py

python analytics/provider_rankings.py
python analytics/provider_health.py
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
python analytics/data_validator.py

python api/metrics.py
python database/init_db.py
python database/import_csv.py
python analytics/daily_report.py
python analytics/research_snapshot.py
python dashboard/dashboard.py
