from fastapi import FastAPI
import pandas as pd
from pathlib import Path
import json

app = FastAPI(
    title="AI-RPCT API",
    description="AI Infrastructure Risk, GPU Stress, Provider Rankings and Forecast API",
    version="3.0"
)

def read_csv(path):
    if Path(path).exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@app.get("/")
def root():
    return {
        "name": "AI-RPCT",
        "status": "online",
        "version": "3.0"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    path = Path("data/api_metrics.json")
    if not path.exists():
        return {"error": "metrics not found"}
    return json.loads(path.read_text())

@app.get("/rpct")
def rpct():
    df = read_csv("data/rpct_scores.csv")
    if df.empty:
        return {"error": "rpct data not found"}
    return df.iloc[-1].to_dict()

@app.get("/forecast")
def forecast():
    df = read_csv("data/forecast_signal.csv")
    if df.empty:
        return {"error": "forecast data not found"}
    return df.iloc[-1].to_dict()

@app.get("/shortage")
def shortage():
    df = read_csv("data/shortage_probability.csv")
    if df.empty:
        return {"error": "shortage data not found"}
    return df.iloc[-1].to_dict()

@app.get("/providers")
def providers():
    df = read_csv("data/provider_rankings.csv")
    if df.empty:
        return []
    return df.to_dict(orient="records")

@app.get("/market")
def market():
    df = read_csv("data/market_data.csv")
    if df.empty:
        return []
    return df.tail(20).to_dict(orient="records")

@app.get("/gpu")
def gpu():
    df = read_csv("data/gpu_data.csv")
    if df.empty:
        return []
    return df.tail(20).to_dict(orient="records")
