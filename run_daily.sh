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
python analytics/data_validator.py
python api/metrics.py
python analytics/daily_report.py
python analytics/research_snapshot.py
python analytics/predictor.py
python analytics/investor_metrics.py
python analytics/executive_dashboard.py
python database/init_db.py
python database/import_csv.py
python dashboard/dashboard.py
