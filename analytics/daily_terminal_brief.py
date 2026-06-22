from datetime import datetime
from pathlib import Path

import pandas as pd


def read_latest(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[-1].to_dict()


def read_first(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return {}
    return pd.read_csv(path).iloc[0].to_dict()


def read_table(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)

Path("reports").mkdir(exist_ok=True)

terminal = read_latest("data/terminal_summary.csv")
signal = read_latest("data/intelligence_signal_score.csv")
frontier = read_latest("data/frontier_gpu_index.csv")
scarcity = read_latest("data/gpu_scarcity_index.csv")
forecast = read_latest("data/forecast_signal.csv")
quality = read_latest("data/core_signal_quality.csv")
readiness = read_latest("data/core_intelligence_readiness.csv")
history_audit = read_latest("data/core_history_audit.csv")
reliability = read_first("data/provider_reliability_ranking.csv")
reliability_gaps = read_table("data/provider_reliability_gaps.csv")
watchlist = read_table("data/gpu_watchlist_intelligence.csv")

top_watch = (
    watchlist.sort_values("avg_price", ascending=False).head(5)
    if not watchlist.empty and "avg_price" in watchlist.columns
    else pd.DataFrame()
)
watchlist_text = (
    top_watch[["gpu", "category", "offers", "avg_price", "min_price", "max_price"]].to_string(index=False)
    if not top_watch.empty
    else "No GPU watchlist data available."
)
top_gaps = (
    reliability_gaps.head(5)[["provider", "priority", "gap", "recommended_action"]].to_string(index=False)
    if not reliability_gaps.empty
    else "No provider reliability gaps available."
)

brief = f"""
AI-RPCT Daily Terminal Brief
Generated: {datetime.now()}

AI Infrastructure Index: {terminal.get('ai_infrastructure_index', 'n/a')}
GPU Price Index: {terminal.get('gpu_price_index', 'n/a')}
GPU Price Trend: {terminal.get('gpu_price_trend', 'n/a')}
Top Provider: {terminal.get('top_provider', 'n/a')}

GPU Scarcity Index: {scarcity.get('gpu_scarcity_index', 'n/a')} ({scarcity.get('scarcity_band', 'n/a')})
Capacity Forecast Score: {forecast.get('forecast_score', 'n/a')} ({forecast.get('capacity_shock_band', 'n/a')})
Provider Reliability Leader: {reliability.get('provider', 'n/a')} ({reliability.get('reliability_score', 'n/a')})
Core Signal Quality: {quality.get('core_signal_quality_score', 'n/a')} ({quality.get('quality_band', 'n/a')})
Core Readiness Phase: {readiness.get('readiness_phase', 'n/a')}
History Progress: {history_audit.get('progress_pct', 'n/a')}% ({history_audit.get('days_remaining', 'n/a')} days remaining)
Signal Blockers: {quality.get('blockers', 'n/a')}
Next Action: {readiness.get('next_action', 'n/a')}

Top Provider Reliability Gaps:
{top_gaps}

Frontier GPU Index: {frontier.get('frontier_gpu_index', 'n/a')}
Frontier Offers: {frontier.get('frontier_offers', 'n/a')}

Intelligence Signal: {signal.get('signal', 'n/a')}
Signal Score: {signal.get('intelligence_signal_score', 'n/a')}

Top Watchlist GPUs:
{watchlist_text}
"""

filename = f"reports/daily_terminal_brief_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(brief)

print(brief)
