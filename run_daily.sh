#!/bin/bash
cd ~/AI-RPCT
source venv/bin/activate

python collectors/collect_market_data.py
python collectors/collect_gpu_data.py
python engine/calculate_rpct.py
python analytics/provider_rankings.py
python dashboard/dashboard.py
