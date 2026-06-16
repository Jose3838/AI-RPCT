import pandas as pd
import matplotlib.pyplot as plt

rpct = pd.read_csv("data/rpct_scores.csv")
gpu = pd.read_csv("data/gpu_data.csv")
market = pd.read_csv("data/market_data.csv")

latest = rpct.iloc[-1]
last_rows = rpct.tail(10)
latest_gpu = gpu.groupby("gpu").last().reset_index()
latest_market = market.groupby("asset").last().reset_index()

plt.figure(figsize=(10, 4))
plt.plot(rpct["score"], marker="o")
plt.title("AI-RPCT Score History")
plt.xlabel("Observation")
plt.ylabel("Score")
plt.ylim(0, 100)
plt.grid(True)
plt.tight_layout()
plt.savefig("data/rpct_chart.png")
plt.close()

score_rows = ""
for _, row in last_rows.iterrows():
    score_rows += f"""
    <tr><td>{row['timestamp']}</td><td>{row['score']}</td><td>{row['regime']}</td><td>{row['drivers']}</td></tr>
    """

gpu_rows = ""
for _, row in latest_gpu.iterrows():
    gpu_rows += f"""
    <tr><td>{row['gpu']}</td><td>{row['provider']}</td><td>${row['price_per_hour']}</td><td>{row['availability']}</td><td>{row['timestamp']}</td></tr>
    """

market_rows = ""
for _, row in latest_market.iterrows():
    market_rows += f"""
    <tr><td>{row['asset']}</td><td>{row['ticker']}</td><td>${row['price']:.4f}</td><td>{row['timestamp']}</td></tr>
    """

html = f"""
<html>
<head>
<title>AI-RPCT Dashboard</title>
<style>
body {{ background:#0b0f19; color:white; font-family:Arial; padding:40px; }}
.grid {{ display:grid; grid-template-columns:420px 1fr; gap:30px; align-items:start; }}
.card {{ background:#111827; padding:30px; border-radius:16px; margin-bottom:30px; }}
.score {{ font-size:72px; font-weight:bold; }}
.regime {{ font-size:28px; margin-top:10px; }}
.drivers {{ margin-top:20px; color:#9ca3af; }}
img {{ width:100%; border-radius:16px; background:white; }}
table {{ width:100%; border-collapse:collapse; background:#111827; border-radius:16px; overflow:hidden; margin-top:20px; margin-bottom:35px; }}
th, td {{ padding:14px; border-bottom:1px solid #1f2937; text-align:left; }}
th {{ color:#9ca3af; }}
</style>
</head>
<body>
<h1>AI-RPCT Dashboard v0.8</h1>

<div class="grid">
  <div class="card">
    <div>Current AI Infrastructure Risk</div>
    <div class="score">{latest["score"]}</div>
    <div class="regime">{latest["regime"]}</div>
    <div class="drivers">Drivers: {latest["drivers"]}</div>
    <br>
    <div>Last update: {latest["timestamp"]}</div>
  </div>

  <div class="card">
    <h2>RPCT History</h2>
    <img src="data/rpct_chart.png">
  </div>
</div>

<h2>Market Snapshot</h2>
<table>
<tr><th>Asset</th><th>Ticker</th><th>Price</th><th>Timestamp</th></tr>
{market_rows}
</table>

<h2>GPU Market Snapshot</h2>
<table>
<tr><th>GPU</th><th>Provider</th><th>Price / Hour</th><th>Availability</th><th>Timestamp</th></tr>
{gpu_rows}
</table>

<h2>Last 10 RPCT Scores</h2>
<table>
<tr><th>Timestamp</th><th>Score</th><th>Regime</th><th>Drivers</th></tr>
{score_rows}
</table>
</body>
</html>
"""

with open("dashboard.html", "w") as f:
    f.write(html)

print("Dashboard v0.8 created: dashboard.html")
