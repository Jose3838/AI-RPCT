import pandas as pd

rpct = pd.read_csv("data/rpct_scores.csv")
latest = rpct.iloc[-1]
last_rows = rpct.tail(10)

rows_html = ""

for _, row in last_rows.iterrows():
    rows_html += f"""
    <tr>
        <td>{row['timestamp']}</td>
        <td>{row['score']}</td>
        <td>{row['regime']}</td>
        <td>{row['drivers']}</td>
    </tr>
    """

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
            width: 420px;
            margin-bottom: 30px;
        }}
        .score {{
            font-size: 72px;
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
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #111827;
            border-radius: 16px;
            overflow: hidden;
        }}
        th, td {{
            padding: 14px;
            border-bottom: 1px solid #1f2937;
            text-align: left;
        }}
        th {{
            color: #9ca3af;
        }}
    </style>
</head>
<body>
    <h1>AI-RPCT Dashboard v0.4</h1>

    <div class="card">
        <div>Current AI Infrastructure Risk</div>
        <div class="score">{latest["score"]}</div>
        <div class="regime">{latest["regime"]}</div>
        <div class="drivers">Drivers: {latest["drivers"]}</div>
        <br>
        <div>Last update: {latest["timestamp"]}</div>
    </div>

    <h2>Last 10 RPCT Scores</h2>

    <table>
        <tr>
            <th>Timestamp</th>
            <th>Score</th>
            <th>Regime</th>
            <th>Drivers</th>
        </tr>
        {rows_html}
    </table>
</body>
</html>
"""

with open("dashboard.html", "w") as f:
    f.write(html)

print("Dashboard v0.4 created: dashboard.html")
