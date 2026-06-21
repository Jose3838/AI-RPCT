from datetime import datetime
import csv
from pathlib import Path

def read_last_rows(file, limit=50):
    p = Path(file)
    if not p.exists():
        return []
    with p.open() as f:
        rows = list(csv.reader(f))
    return rows[-limit:]

def market_regime():
    rows = read_last_rows("provider_momentum_history.csv")
    scores = []
    for r in rows:
        try:
            scores.append(float(r[2]))
        except:
            pass

    avg = round(sum(scores) / len(scores), 2) if scores else 0

    if avg >= 30:
        regime = "strong_competitive_market"
    elif avg >= 20:
        regime = "competitive_market"
    elif avg >= 10:
        regime = "fragmented_market"
    else:
        regime = "weak_market"

    return {
        "market_regime": regime,
        "average_provider_momentum": avg,
        "generated_at": datetime.utcnow().isoformat()
    }

def provider_strength():
    rows = read_last_rows("provider_momentum_history.csv")
    latest = {}

    for r in rows:
        try:
            latest[r[1]] = {
                "provider": r[1],
                "strength_score": float(r[2]),
                "position": r[3]
            }
        except:
            pass

    return sorted(latest.values(), key=lambda x: x["strength_score"], reverse=True)

def early_warning():
    providers = provider_strength()
    result = []

    for p in providers:
        score = p["strength_score"]
        if score < 5:
            level = "critical"
        elif score < 15:
            level = "watch"
        else:
            level = "normal"

        result.append({
            "provider": p["provider"],
            "warning_level": level,
            "strength_score": score
        })

    return result

def market_signal():
    strengths = provider_strength()
    avg = round(sum(p["strength_score"] for p in strengths) / len(strengths), 2) if strengths else 0

    if avg >= 25:
        direction = "bullish"
    elif avg >= 15:
        direction = "neutral"
    else:
        direction = "stress"

    return {
        "market_signal_score": avg,
        "market_direction": direction,
        "generated_at": datetime.utcnow().isoformat()
    }

def snapshot_v4():
    return {
        "system": "AI-RPCT",
        "snapshot_version": "v4",
        "stage": "gpu_market_intelligence",
        "market_regime": market_regime(),
        "provider_strength": provider_strength(),
        "early_warning": early_warning(),
        "market_signal": market_signal(),
        "generated_at": datetime.utcnow().isoformat()
    }
