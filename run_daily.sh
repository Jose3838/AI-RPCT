#!/bin/bash
cd ~/AI-RPCT
source venv/bin/activate

python collectors/collect_market_data.py
python collectors/collect_gpu_data.py
python engine/calculate_rpct.py
python analytics/provider_rankings.py
python analytics/shortage_probability.py
python analytics/forecast_signal.py
python analytics/trend_engine.py
python api/metrics.py
python analytics/daily_report.py
python dashboard/dashboard.py
