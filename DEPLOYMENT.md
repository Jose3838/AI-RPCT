# AI-RPCT Deployment

## Local API

```bash
./start_api.sh
http://127.0.0.1:8000/docs
cd ~/AI-RPCT
source venv/bin/activate

# v10.0 Investor dashboard data
cat > analytics/investor_dashboard.py << 'EOF'
import pandas as pd
from pathlib import Path

rpct = pd.read_csv("data/rpct_scores.csv").iloc[-1]
forecast = pd.read_csv("data/forecast_signal.csv").iloc[-1]
shortage = pd.read_csv("data/shortage_probability.csv").iloc[-1]
providers = pd.read_csv("data/provider_rankings.csv")

top_provider = providers.sort_values("score", ascending=False).iloc[0]

data = pd.DataFrame([{
    "rpct_score": rpct["score"],
    "regime": rpct["regime"],
    "forecast_score": forecast["forecast_score"],
    "outlook": forecast["outlook"],
    "shortage_probability": shortage["shortage_probability"],
    "top_provider": top_provider["provider"],
    "top_provider_score": top_provider["score"]
}])

Path("data").mkdir(exist_ok=True)
data.to_csv("data/investor_dashboard.csv", index=False)

print(data)
