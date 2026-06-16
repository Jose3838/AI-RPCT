import pandas as pd

rpct = pd.read_csv("data/rpct_scores.csv")
latest = rpct.iloc[-1]

html = f"""
<html>
<head>
    <title>AI-RPCT Dashboard</title>
    <style>
        body {{
            background: #0b0f19;
            color: white;
            font-family: Arial;
            padding: 40px;
        }}
        .card {{
            background: #111827;
            padding: 30px;
            border-radius: 16px;
            width: 400px;
        }}
        .score {{
            font-size: 64px;
            font-weight: bold;
        }}
        .regime {{
            font-size: 28px;
            margin-top: 10px;
        }}
        .drivers {{
            margin-top: 20px;
            color: #9ca3af;
        }}
    </style>
</head>
<body>
    <h1>AI-RPCT Dashboard</h1>

    <div class="card">
        <div>Current AI Infrastructure Risk</div>
        <div class="score">{latest["score"]}</div>
        <div class="regime">{latest["regime"]}</div>
        <div class="drivers">Drivers: {latest["drivers"]}</div>
        <br>
        <div>Last update: {latest["timestamp"]}</div>
    </div>
</body>
</html>
"""

with open("dashboard.html", "w") as f:
    f.write(html)

print("Dashboard created: dashboard.html")
