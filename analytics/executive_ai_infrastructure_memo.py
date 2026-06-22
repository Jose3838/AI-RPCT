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

risk = read_latest("data/terminal_risk_score.csv")
summary = read_latest("data/terminal_summary.csv")
frontier = read_latest("data/frontier_gpu_index.csv")
scarcity = read_latest("data/gpu_scarcity_index.csv")
forecast = read_latest("data/forecast_signal.csv")
quality = read_latest("data/core_signal_quality.csv")
readiness = read_latest("data/core_intelligence_readiness.csv")
reliability = read_first("data/provider_reliability_ranking.csv")
reliability_gaps = read_table("data/provider_reliability_gaps.csv")
category = read_table("data/gpu_category_index.csv")
category_text = category.to_string(index=False) if not category.empty else "No GPU category data available."
top_gaps = (
    reliability_gaps.head(5)[["provider", "priority", "gap", "recommended_action"]].to_string(index=False)
    if not reliability_gaps.empty
    else "No provider reliability gaps available."
)

memo = f"""
AI-RPCT Executive AI Infrastructure Memo
Generated: {datetime.now()}

Overall Risk Level: {risk.get('risk_level', 'n/a')}
Terminal Risk Score: {risk.get('terminal_risk_score', 'n/a')}

AI Infrastructure Index: {summary.get('ai_infrastructure_index', 'n/a')}
GPU Price Index: {summary.get('gpu_price_index', 'n/a')}
GPU Price Trend: {summary.get('gpu_price_trend', 'n/a')}
Top Provider: {summary.get('top_provider', 'n/a')}

Core Intelligence:
GPU Scarcity Index: {scarcity.get('gpu_scarcity_index', 'n/a')} ({scarcity.get('scarcity_band', 'n/a')})
Capacity Forecast Score: {forecast.get('forecast_score', 'n/a')} ({forecast.get('capacity_shock_band', 'n/a')})
Top Provider Reliability: {reliability.get('provider', 'n/a')} ({reliability.get('reliability_score', 'n/a')})
Core Signal Quality: {quality.get('core_signal_quality_score', 'n/a')} ({quality.get('quality_band', 'n/a')})
Core Readiness Phase: {readiness.get('readiness_phase', 'n/a')}
Paid Beta Signal Ready: {quality.get('paid_beta_signal_ready', 'n/a')}
Signal Blockers: {quality.get('blockers', 'n/a')}
Next Action: {readiness.get('next_action', 'n/a')}

Top Provider Reliability Gaps:
{top_gaps}

Frontier GPU Index: {frontier.get('frontier_gpu_index', 'n/a')}
Frontier Offers: {frontier.get('frontier_offers', 'n/a')}

GPU Category Index:
{category_text}

Interpretation:
AI-RPCT monitors live GPU market data, provider health, pricing signals, scarcity indicators and infrastructure risk signals. The strongest product asset is the daily time series of scarcity, shock forecast and provider reliability.
"""

filename = f"reports/executive_ai_infrastructure_memo_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w") as f:
    f.write(memo)

print(memo)
