import pandas as pd
from datetime import datetime
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

terminal = pd.read_csv("data/terminal_summary.csv").iloc[-1]
signal = pd.read_csv("data/intelligence_signal_score.csv").iloc[-1]
frontier = pd.read_csv("data/frontier_gpu_index.csv").iloc[-1]
watchlist = pd.read_csv("data/gpu_watchlist_intelligence.csv")

top_watch = watchlist.sort_values("avg_price", ascending=False).head(5)

brief = f"""
AI-RPCT Daily Terminal Brief
Generated: {datetime.now()}

AI Infrastructure Index: {terminal['ai_infrastructure_index']}
GPU Price Index: {terminal['gpu_price_index']}
GPU Price Trend: {terminal['gpu_price_trend']}
Top Provider: {terminal['top_provider']}

Frontier GPU Index: {frontier['frontier_gpu_index']}
Frontier Offers: {frontier['frontier_offers']}

Intelligence Signal: {signal['signal']}
Signal Score: {signal['intelligence_signal_score']}

Top Watchlist GPUs:
{top_watch[['gpu','category','offers','avg_price','min_price','max_price']].to_string(index=False)}
"""

filename = f"reports/daily_terminal_brief_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(brief)

print(brief)
