from fastapi import APIRouter, Header

router = APIRouter()


@router.get("/usage-analytics")
def usage_analytics():
    import pandas as pd
    from pathlib import Path

    path = Path("data/usage_metrics.csv")

    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")


@router.post("/admin/run-history-snapshot")
def admin_run_history_snapshot():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "jobs/history_snapshot.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "error",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


@router.get("/gpu-forecast-signal")
def gpu_forecast_signal():
    import pandas as pd
    from pathlib import Path

    path = Path("data/gpu_price_forecast_signal.csv")

    if not path.exists():
        return []

    return pd.read_csv(path).to_dict(orient="records")


@router.post("/admin/run-forecasting-engine")
def admin_run_forecasting_engine():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "analytics/forecasting_engine.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "error",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


@router.get("/gpu-forecast-signal-safe")
def gpu_forecast_signal_safe():
    import pandas as pd
    from pathlib import Path

    path = Path("data/gpu_price_forecast_signal.csv")

    if not path.exists():
        return [{
            "signal": "no_file",
            "trend": "unknown",
            "volatility": 0,
            "latest_price_index": None,
            "previous_price_index": None,
            "change_pct": None
        }]

    try:
        return pd.read_csv(path).to_dict(orient="records")
    except Exception as e:
        return [{
            "signal": "read_error",
            "trend": "unknown",
            "error": str(e)
        }]


@router.get("/gpu-forecast-signal-v2")
def gpu_forecast_signal_v2():
    import csv
    from pathlib import Path

    path = Path("data/gpu_price_forecast_signal.csv")

    if not path.exists():
        return [{
            "signal": "no_file",
            "trend": "unknown",
            "volatility": 0,
            "latest_price_index": None,
            "previous_price_index": None,
            "change_pct": None
        }]

    rows = []
    with path.open("r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean = {}
            for k, v in row.items():
                if v == "" or v == "nan" or v == "NaN":
                    clean[k] = None
                else:
                    clean[k] = v
            rows.append(clean)

    return rows


@router.post("/admin/generate-test-history")
def admin_generate_test_history(points: int = 50):
    import pandas as pd
    from pathlib import Path
    from datetime import datetime, timedelta, timezone
    import random

    Path("data").mkdir(exist_ok=True)

    now = datetime.now(timezone.utc)
    rows = []

    base_price = 4.45

    for i in range(points):
        ts = now - timedelta(hours=points - i)
        price = round(base_price + random.uniform(-0.55, 0.55), 4)

        rows.append({
            "timestamp": ts.isoformat(),
            "date": ts.date().isoformat(),
            "gpu_price_index": price,
            "offers": random.randint(80, 140),
            "synthetic": True
        })

    df = pd.DataFrame(rows)
    path = Path("data/gpu_price_history.csv")

    if path.exists():
        old = pd.read_csv(path)
        combined = pd.concat([old, df], ignore_index=True)
    else:
        combined = df

    combined.to_csv(path, index=False)

    return {
        "status": "success",
        "generated_points": points,
        "file": "data/gpu_price_history.csv",
        "total_rows": len(combined),
        "note": "synthetic test history added for forecasting/demo readiness"
    }


@router.get("/market-intelligence-report-v1")
def market_intelligence_report_v1():
    import pandas as pd
    from pathlib import Path
    from datetime import datetime, timezone

    forecast_path = Path("data/gpu_price_forecast_signal.csv")
    coverage_path = Path("data/provider_registry.csv")
    history_path = Path("data/gpu_price_history.csv")

    if forecast_path.exists():
        forecast = pd.read_csv(forecast_path).iloc[-1].to_dict()
    else:
        forecast = {
            "signal": "no_data",
            "trend": "unknown",
            "volatility": 0,
            "change_pct": None
        }

    live_providers = 0
    total_providers = 0

    if coverage_path.exists():
        providers = pd.read_csv(coverage_path)
        total_providers = len(providers)
        live_providers = len(providers[providers["live"] == True])

    history_rows = 0
    synthetic_rows = 0

    if history_path.exists():
        history = pd.read_csv(history_path)
        history_rows = len(history)
        if "synthetic" in history.columns:
            synthetic_rows = len(history[history["synthetic"] == True])

    signal = str(forecast.get("signal", "unknown"))
    trend = str(forecast.get("trend", "unknown"))
    change_pct = forecast.get("change_pct", None)
    volatility = forecast.get("volatility", 0)

    if signal == "watch":
        headline = "GPU infrastructure market shows elevated price movement."
        interpretation = "Recent GPU price index movement indicates a potential short-term price spike."
    elif signal == "opportunity":
        headline = "GPU infrastructure market shows potential buying opportunity."
        interpretation = "Recent GPU price index movement indicates a short-term price drop."
    elif signal == "normal":
        headline = "GPU infrastructure market remains stable."
        interpretation = "Recent GPU price index movement is within normal range."
    else:
        headline = "GPU infrastructure intelligence is collecting more data."
        interpretation = "Forecast confidence is limited until more historical data is available."

    return {
        "product": "AI-RPCT",
        "mission": "Bloomberg for AI Infrastructure",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "interpretation": interpretation,
        "market_signal": signal,
        "trend": trend,
        "change_pct": change_pct,
        "volatility": volatility,
        "provider_coverage": {
            "live_providers": live_providers,
            "total_target_providers": total_providers,
            "coverage_pct": round((live_providers / total_providers) * 100, 2) if total_providers else 0
        },
        "data_moat": {
            "history_rows": history_rows,
            "synthetic_rows": synthetic_rows,
            "real_rows": history_rows - synthetic_rows
        },
        "recommended_action": "Monitor provider pricing and continue expanding historical snapshots."
    }


@router.get("/market-intelligence-report-v2")
def market_intelligence_report_v2():
    import csv
    from pathlib import Path
    from datetime import datetime, timezone

    def read_last_csv_row(path):
        p = Path(path)
        if not p.exists():
            return {}
        with p.open("r") as f:
            rows = list(csv.DictReader(f))
            return rows[-1] if rows else {}

    def read_csv_rows(path):
        p = Path(path)
        if not p.exists():
            return []
        with p.open("r") as f:
            return list(csv.DictReader(f))

    def clean(v):
        if v in ["", "nan", "NaN", None]:
            return None
        return v

    forecast = read_last_csv_row("data/gpu_price_forecast_signal.csv")
    providers = read_csv_rows("data/provider_registry.csv")
    history = read_csv_rows("data/gpu_price_history.csv")

    live_providers = len([p for p in providers if str(p.get("live")).lower() == "true"])
    total_providers = len(providers)

    history_rows = len(history)
    synthetic_rows = len([r for r in history if str(r.get("synthetic")).lower() == "true"])

    signal = clean(forecast.get("signal")) or "no_data"
    trend = clean(forecast.get("trend")) or "unknown"
    change_pct = clean(forecast.get("change_pct"))
    volatility = clean(forecast.get("volatility"))

    if signal == "watch":
        headline = "GPU infrastructure market shows elevated price movement."
        interpretation = "Recent GPU price index movement indicates a potential short-term price spike."
    elif signal == "opportunity":
        headline = "GPU infrastructure market shows potential buying opportunity."
        interpretation = "Recent GPU price index movement indicates a short-term price drop."
    elif signal == "normal":
        headline = "GPU infrastructure market remains stable."
        interpretation = "Recent GPU price index movement is within normal range."
    else:
        headline = "GPU infrastructure intelligence is collecting more data."
        interpretation = "Forecast confidence is limited until more historical data is available."

    return {
        "product": "AI-RPCT",
        "mission": "Bloomberg for AI Infrastructure",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "interpretation": interpretation,
        "market_signal": signal,
        "trend": trend,
        "change_pct": change_pct,
        "volatility": volatility,
        "provider_coverage": {
            "live_providers": live_providers,
            "total_target_providers": total_providers,
            "coverage_pct": round((live_providers / total_providers) * 100, 2) if total_providers else 0
        },
        "data_moat": {
            "history_rows": history_rows,
            "synthetic_rows": synthetic_rows,
            "real_rows": history_rows - synthetic_rows
        },
        "recommended_action": "Monitor provider pricing and continue expanding historical snapshots."
    }


@router.get("/enterprise-report-v1")
def enterprise_report_v1():
    import csv
    from pathlib import Path
    from datetime import datetime, timezone

    forecast = {}

    fp = Path("data/gpu_price_forecast_signal.csv")
    if fp.exists():
        with fp.open() as f:
            rows = list(csv.DictReader(f))
            if rows:
                forecast = rows[-1]

    signal = forecast.get("signal", "unknown")
    trend = forecast.get("trend", "unknown")
    change_pct = forecast.get("change_pct")

    if signal == "opportunity":
        executive_summary = (
            "GPU pricing weakened in the latest observation window. "
            "Infrastructure buyers may find favorable purchasing conditions."
        )
    elif signal == "watch":
        executive_summary = (
            "GPU pricing accelerated in the latest observation window. "
            "Infrastructure costs may increase if momentum continues."
        )
    else:
        executive_summary = (
            "GPU infrastructure pricing remains within expected ranges."
        )

    return {
        "report_type": "enterprise_intelligence",
        "product": "AI-RPCT",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "executive_summary": executive_summary,
        "market_signal": signal,
        "trend": trend,
        "change_pct": change_pct,
        "coverage": {
            "live_providers": 2,
            "target_providers": 6
        },
        "recommendation": (
            "Continue monitoring GPU pricing, provider health and "
            "market-share changes."
        )
    }


@router.get("/enterprise-report-v2")
def enterprise_report_v2(x_api_key: str = Header(default=None)):
    import csv
    from pathlib import Path
    from datetime import datetime, timezone
    from security.plan_resolver import resolve_plan

    plan = resolve_plan(x_api_key)

    if plan != "enterprise":
        return {
            "allowed": False,
            "required_plan": "enterprise",
            "current_plan": plan,
            "message": "Enterprise report requires enterprise access."
        }

    forecast = {}
    fp = Path("data/gpu_price_forecast_signal.csv")

    if fp.exists():
        with fp.open() as f:
            rows = list(csv.DictReader(f))
            if rows:
                forecast = rows[-1]

    signal = forecast.get("signal", "unknown")
    trend = forecast.get("trend", "unknown")
    change_pct = forecast.get("change_pct")
    volatility = forecast.get("volatility")

    if signal == "opportunity":
        executive_summary = (
            "GPU pricing weakened in the latest observation window. "
            "Infrastructure buyers may find favorable purchasing conditions."
        )
    elif signal == "watch":
        executive_summary = (
            "GPU pricing accelerated in the latest observation window. "
            "Infrastructure costs may increase if momentum continues."
        )
    elif signal == "normal":
        executive_summary = (
            "GPU infrastructure pricing remains stable in the latest observation window."
        )
    else:
        executive_summary = (
            "GPU infrastructure intelligence is collecting additional history "
            "before issuing a stronger market view."
        )

    return {
        "allowed": True,
        "plan": plan,
        "report_type": "enterprise_intelligence",
        "product": "AI-RPCT",
        "mission": "Bloomberg for AI Infrastructure",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "executive_summary": executive_summary,
        "market_signal": signal,
        "trend": trend,
        "change_pct": change_pct,
        "volatility": volatility,
        "coverage": {
            "live_providers": 2,
            "target_providers": 6
        },
        "recommendation": (
            "Monitor GPU pricing, provider health, market-share changes "
            "and continue building historical infrastructure data."
        )
    }
