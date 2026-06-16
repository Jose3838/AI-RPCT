import pandas as pd

rpct = pd.read_csv("data/rpct_scores.csv")

if len(rpct) < 2:
    trend = "INSUFFICIENT_DATA"
else:
    current = float(rpct.iloc[-1]["score"])
    previous = float(rpct.iloc[-2]["score"])

    if current > previous:
        trend = "RISK_INCREASING"
    elif current < previous:
        trend = "RISK_DECREASING"
    else:
        trend = "STABLE"

result = pd.DataFrame([{
    "trend": trend
}])

result.to_csv("data/trend_signal.csv", index=False)

print(result)
