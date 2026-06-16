#!/bin/bash
cd ~/AI-RPCT
source venv/bin/activate

python collect_market_data.py
python collect_gpu_data.py
python calculate_rpct.py
python dashboard.py
