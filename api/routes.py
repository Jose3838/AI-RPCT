from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter()

def read_csv(path):
    if not Path(path).exists():
        return []
    return pd.read_csv(path).to_dict(orient="records")

@router.get("/rankings")
def rankings():
    return read_csv("data/provider_rankings.csv")

@router.get("/forecast")
def forecast():
    return read_csv("data/forecast_signal.csv")

@router.get("/rpct")
def rpct():
    return read_csv("data/rpct_scores.csv")

@router.get("/shortage")
def shortage():
    return read_csv("data/shortage_probability.csv")
