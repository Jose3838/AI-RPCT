from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
MARKET_PULSE_HISTORY_FILE = DATA_DIR / "market_pulse_history.csv"


def read_records(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size <= 1:
        return []
    return pd.read_csv(path).to_dict(orient="records")


def read_latest(path):
    records = read_records(path)
    if not records:
        return {}
    return records[-1]


def read_latest_report(pattern):
    reports = sorted(REPORTS_DIR.glob(pattern))
    if not reports:
        return {
            "status": "missing",
            "file": None,
            "content": ""
        }

    latest = reports[-1]
    return {
        "status": "ok",
        "file": latest.name,
        "content": latest.read_text()
    }


def as_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, value))


def score_band(score):
    score = as_float(score)
    if score >= 80:
        return "critical"
    if score >= 60:
        return "elevated"
    if score >= 35:
        return "watch"
    return "stable"


def confidence_band(score):
    score = as_float(score)
    if score >= 80:
        return "high"
    if score >= 60:
        return "medium"
    if score >= 35:
        return "low"
    return "thin"


def make_signal(signal_type, severity, title, message, evidence):
    return {
        "type": signal_type,
        "severity": severity,
        "title": title,
        "message": message,
        "evidence": evidence
    }


def build_market_signals():
    terminal = read_latest(DATA_DIR / "terminal_summary.csv")
    risk = read_latest(DATA_DIR / "terminal_risk_score.csv")
    trend = read_latest(DATA_DIR / "gpu_price_trend_signal.csv")
    forecast = read_latest(DATA_DIR / "forecast_signal.csv")
    scarcity_index = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    cheapest = read_records(DATA_DIR / "live_gpu_cheapest.csv")
    expensive = read_records(DATA_DIR / "live_gpu_most_expensive.csv")
    scarcity = read_records(DATA_DIR / "scarcity_watchlist.csv")
    provider_health = read_records(DATA_DIR / "provider_health.csv")
    provider_reliability = read_records(DATA_DIR / "provider_reliability_ranking.csv")

    signals = []
    risk_score = as_float(risk.get("terminal_risk_score"))
    price_trend = str(trend.get("gpu_price_trend_signal", terminal.get("gpu_price_trend", "unknown")))
    change_pct = as_float(trend.get("change_pct"))

    if risk_score >= 80:
        signals.append(make_signal(
            "risk",
            "high",
            "Infrastructure risk is elevated",
            "Risk is high enough that buyers should monitor capacity and provider reliability before committing spend.",
            {"terminal_risk_score": risk_score}
        ))
    elif risk_score >= 60:
        signals.append(make_signal(
            "risk",
            "medium",
            "Risk is in watch mode",
            "The market is not calm, but current conditions do not require immediate escalation.",
            {"terminal_risk_score": risk_score}
        ))
    else:
        signals.append(make_signal(
            "risk",
            "low",
            "Risk is contained",
            "Current infrastructure risk is within the lower operating range.",
            {"terminal_risk_score": risk_score}
        ))

    if "down" in price_trend or change_pct <= -5:
        signals.append(make_signal(
            "opportunity",
            "medium",
            "GPU price pressure is easing",
            "Recent price movement may create a buying window for flexible workloads.",
            {"gpu_price_trend": price_trend, "change_pct": change_pct}
        ))
    elif "up" in price_trend or change_pct >= 5:
        signals.append(make_signal(
            "cost",
            "high",
            "GPU price pressure is rising",
            "Rising pricing pressure may increase short-term infrastructure costs.",
            {"gpu_price_trend": price_trend, "change_pct": change_pct}
        ))
    else:
        signals.append(make_signal(
            "market",
            "low",
            "GPU pricing is stable",
            "Pricing is not showing a strong directional move in the latest observation window.",
            {"gpu_price_trend": price_trend, "change_pct": change_pct}
        ))

    if cheapest:
        best = cheapest[0]
        signals.append(make_signal(
            "buying_signal",
            "low",
            f"Cheapest tracked GPU: {best.get('gpu', 'unknown')}",
            "This GPU currently offers the lowest average tracked price.",
            {
                "gpu": best.get("gpu"),
                "avg_price": best.get("avg_price"),
                "min_price": best.get("min_price"),
                "offers": best.get("offers")
            }
        ))

    if expensive:
        top = expensive[0]
        signals.append(make_signal(
            "premium_pressure",
            "medium",
            f"Most expensive tracked GPU: {top.get('gpu', 'unknown')}",
            "High average pricing here can indicate frontier demand pressure or limited supply.",
            {
                "gpu": top.get("gpu"),
                "avg_price": top.get("avg_price"),
                "max_price": top.get("max_price"),
                "offers": top.get("offers")
            }
        ))

    scarce_frontier = [
        row for row in scarcity
        if str(row.get("category", "")).lower() == "frontier"
        and str(row.get("scarcity_flag", "")).lower() == "true"
    ]
    if scarce_frontier:
        signals.append(make_signal(
            "scarcity",
            "high",
            "Frontier GPU scarcity detected",
            "One or more frontier GPUs are flagged as scarce and should be watched closely.",
            {
                "gpus": [row.get("gpu") for row in scarce_frontier[:5]],
                "count": len(scarce_frontier)
            }
        ))

    scarcity_score = as_float(scarcity_index.get("gpu_scarcity_index"))
    if scarcity_score >= 70:
        scarcity_severity = "high"
    elif scarcity_score >= 45:
        scarcity_severity = "medium"
    else:
        scarcity_severity = "low"

    signals.append(make_signal(
        "gpu_scarcity_index",
        scarcity_severity,
        f"GPU Scarcity Index is {scarcity_score}",
        "The scarcity index blends availability pressure, price pressure, frontier GPU pressure and provider depth.",
        {
            "gpu_scarcity_index": scarcity_score,
            "scarcity_band": scarcity_index.get("scarcity_band"),
            "availability_pressure_score": scarcity_index.get("availability_pressure_score"),
            "price_pressure_score": scarcity_index.get("price_pressure_score"),
            "frontier_pressure_score": scarcity_index.get("frontier_pressure_score"),
            "provider_depth_score": scarcity_index.get("provider_depth_score"),
        }
    ))

    forecast_score = as_float(forecast.get("forecast_score"))
    shock_band_value = forecast.get("capacity_shock_band", "stable")
    shock_delta = as_float(forecast.get("capacity_shock_delta"))
    if shock_band_value in {"shock_up", "rising"} or forecast_score >= 70:
        severity = "high" if shock_band_value == "shock_up" or forecast_score >= 80 else "medium"
        title = "Capacity shock risk is rising"
    elif shock_band_value in {"shock_down", "easing"}:
        severity = "medium"
        title = "Capacity pressure is easing"
    else:
        severity = "low"
        title = "Capacity shock forecast is stable"

    signals.append(make_signal(
        "capacity_shock_forecast",
        severity,
        title,
        "The forecast combines RPCT pressure, shortage probability, scarcity and recent shock delta.",
        {
            "forecast_score": forecast_score,
            "outlook": forecast.get("outlook"),
            "capacity_shock_delta": shock_delta,
            "capacity_shock_band": shock_band_value,
            "confidence_score": forecast.get("confidence_score"),
        }
    ))

    offline = [row.get("provider") for row in provider_health if row.get("status") != "online"]
    if offline:
        signals.append(make_signal(
            "provider_health",
            "medium",
            "Provider health needs attention",
            "At least one tracked provider is not currently reporting as online.",
            {"offline_providers": offline}
        ))

    weak_providers = [
        row for row in provider_reliability
        if as_float(row.get("reliability_score")) < 60
    ]
    if weak_providers:
        signals.append(make_signal(
            "provider_reliability",
            "medium",
            "Provider Reliability Score needs attention",
            "One or more providers have weak reliability scores based on freshness, depth, availability and stability.",
            {
                "providers": [
                    {
                        "provider": row.get("provider"),
                        "reliability_score": row.get("reliability_score"),
                        "reliability_band": row.get("reliability_band"),
                    }
                    for row in weak_providers[:5]
                ],
                "count": len(weak_providers),
            }
        ))

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "signals": signals,
        "signal_count": len(signals)
    }


def build_market_pulse():
    summary = build_terminal_summary()
    signals = build_market_signals()["signals"]

    terminal = summary.get("terminal", {})
    risk = summary.get("risk", {})
    quality = summary.get("quality", {})
    scarcity = summary.get("scarcity", {})
    frontier = summary.get("frontier", {})
    moat = read_latest(DATA_DIR / "data_moat_score.csv")

    risk_score = as_float(risk.get("terminal_risk_score"))
    scarcity_score = as_float(scarcity.get("gpu_scarcity_index"))
    data_quality = as_float(quality.get("live_data_quality_score"))
    data_moat = as_float(moat.get("data_moat_score"))
    frontier_index = as_float(frontier.get("frontier_gpu_index"))
    active_alerts = as_float(terminal.get("active_alerts"))

    pricing_pressure = 50.0
    trend = str(terminal.get("gpu_price_trend", "stable")).lower()
    if "up" in trend:
        pricing_pressure = 75.0
    elif "down" in trend:
        pricing_pressure = 35.0
    elif terminal.get("gpu_price_index") not in (None, ""):
        pricing_pressure = clamp(45.0 + as_float(terminal.get("gpu_price_index")) * 2.0)

    market_pulse_score = round(clamp(
        (risk_score * 0.35)
        + (scarcity_score * 0.25)
        + (pricing_pressure * 0.20)
        + (frontier_index * 0.10)
        + (active_alerts * 5.0)
        + ((100.0 - data_quality) * 0.10)
    ), 2)

    confidence_score = round(clamp((data_quality * 0.60) + (data_moat * 0.40)), 2)
    severity_counts = {}
    for signal in signals:
        severity = signal.get("severity", "unknown")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    if market_pulse_score >= 80:
        headline = "AI infrastructure market is in critical pressure mode."
        buyer_readout = "Delay non-urgent commitments, validate provider alternatives, and protect scarce frontier capacity."
        investor_readout = "Market stress is high enough to support close monitoring of provider concentration and pricing power."
    elif market_pulse_score >= 60:
        headline = "AI infrastructure market pressure is elevated."
        buyer_readout = "Benchmark providers before buying capacity and keep a fallback plan for high-priority workloads."
        investor_readout = "The market is showing investable pressure, but confidence depends on continued live-data depth."
    elif market_pulse_score >= 35:
        headline = "AI infrastructure market is in watch mode."
        buyer_readout = "Track price and scarcity movement, but avoid overreacting to a single observation window."
        investor_readout = "Signals are forming; more historical observations will improve conviction."
    else:
        headline = "AI infrastructure market pressure is contained."
        buyer_readout = "Current conditions support normal procurement with routine provider comparison."
        investor_readout = "Stress signals are limited; monitor for inflection rather than immediate action."

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "market_pulse",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "market_pulse_score": market_pulse_score,
        "market_pulse_band": score_band(market_pulse_score),
        "confidence_score": confidence_score,
        "confidence_band": confidence_band(confidence_score),
        "drivers": {
            "terminal_risk_score": risk_score,
            "gpu_scarcity_index": scarcity_score,
            "pricing_pressure": round(pricing_pressure, 2),
            "frontier_gpu_index": frontier_index,
            "active_alerts": active_alerts,
            "live_data_quality_score": data_quality,
            "data_moat_score": data_moat,
        },
        "signal_summary": {
            "signal_count": len(signals),
            "severity_counts": severity_counts,
        },
        "audience_readouts": {
            "buyers": buyer_readout,
            "investors": investor_readout,
        },
        "next_best_actions": [
            "Compare provider depth before committing GPU spend.",
            "Monitor frontier GPU scarcity and live provider health.",
            "Use Pro recommendations for account-specific procurement actions.",
        ],
    }


def market_pulse_history_row(pulse):
    drivers = pulse.get("drivers", {})
    return {
        "timestamp": pulse.get("generated_at"),
        "market_pulse_score": pulse.get("market_pulse_score"),
        "market_pulse_band": pulse.get("market_pulse_band"),
        "confidence_score": pulse.get("confidence_score"),
        "confidence_band": pulse.get("confidence_band"),
        "terminal_risk_score": drivers.get("terminal_risk_score"),
        "gpu_scarcity_index": drivers.get("gpu_scarcity_index"),
        "pricing_pressure": drivers.get("pricing_pressure"),
        "frontier_gpu_index": drivers.get("frontier_gpu_index"),
        "active_alerts": drivers.get("active_alerts"),
        "live_data_quality_score": drivers.get("live_data_quality_score"),
        "data_moat_score": drivers.get("data_moat_score"),
        "headline": pulse.get("headline"),
    }


def save_market_pulse_snapshot(pulse=None, history_file=MARKET_PULSE_HISTORY_FILE):
    pulse = pulse or build_market_pulse()
    row = pd.DataFrame([market_pulse_history_row(pulse)])
    path = Path(history_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > 1:
        history = pd.read_csv(path)
        history = pd.concat([history, row], ignore_index=True)
    else:
        history = row

    history.to_csv(path, index=False)

    return {
        "status": "saved",
        "file": str(path),
        "timestamp": pulse.get("generated_at"),
        "market_pulse_score": pulse.get("market_pulse_score"),
        "market_pulse_band": pulse.get("market_pulse_band"),
    }


def build_market_pulse_history(limit=30):
    records = read_records(MARKET_PULSE_HISTORY_FILE)
    if limit:
        records = records[-int(limit):]

    latest = records[-1] if records else {}
    previous = records[-2] if len(records) >= 2 else {}
    delta = round(
        as_float(latest.get("market_pulse_score")) - as_float(previous.get("market_pulse_score")),
        2,
    ) if latest and previous else 0.0

    direction = "flat"
    if delta > 0:
        direction = "up"
    elif delta < 0:
        direction = "down"

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "market_pulse_history",
        "record_count": len(records),
        "latest": latest,
        "previous": previous,
        "trend": {
            "delta": delta,
            "direction": direction,
        },
        "history": records,
    }


def build_market_pulse_brief():
    pulse = build_market_pulse()
    history = build_market_pulse_history()
    drivers = pulse.get("drivers", {})
    readouts = pulse.get("audience_readouts", {})
    trend = history.get("trend", {})
    delta = as_float(trend.get("delta"))
    direction = trend.get("direction", "flat")

    if direction == "up":
        trend_summary = f"Market pressure increased by {delta} points versus the previous pulse snapshot."
    elif direction == "down":
        trend_summary = f"Market pressure decreased by {abs(delta)} points versus the previous pulse snapshot."
    elif history.get("record_count", 0) >= 2:
        trend_summary = "Market pressure is flat versus the previous pulse snapshot."
    else:
        trend_summary = "Market pulse history is still building; trend conviction is limited until more snapshots exist."

    driver_lines = [
        f"Terminal risk score is {drivers.get('terminal_risk_score', 'n/a')}.",
        f"GPU scarcity index is {drivers.get('gpu_scarcity_index', 'n/a')}.",
        f"Pricing pressure is {drivers.get('pricing_pressure', 'n/a')}.",
        f"Frontier GPU index is {drivers.get('frontier_gpu_index', 'n/a')}.",
        f"Live data quality is {drivers.get('live_data_quality_score', 'n/a')}.",
        f"Data moat score is {drivers.get('data_moat_score', 'n/a')}.",
    ]

    markdown = [
        "# AI-RPCT Market Pulse Brief",
        "",
        f"Generated: {pulse.get('generated_at')}",
        "",
        "## Headline",
        pulse.get("headline", ""),
        "",
        "## Pulse",
        f"- Market Pulse Score: {pulse.get('market_pulse_score')} ({pulse.get('market_pulse_band')})",
        f"- Confidence Score: {pulse.get('confidence_score')} ({pulse.get('confidence_band')})",
        f"- Trend: {direction} ({delta})",
        "",
        "## Trend Summary",
        trend_summary,
        "",
        "## Driver Readout",
        *[f"- {line}" for line in driver_lines],
        "",
        "## Buyer Readout",
        readouts.get("buyers", ""),
        "",
        "## Investor Readout",
        readouts.get("investors", ""),
        "",
        "## Next Best Actions",
        *[f"- {item}" for item in pulse.get("next_best_actions", [])],
    ]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "market_pulse_brief",
        "generated_at": pulse.get("generated_at"),
        "headline": pulse.get("headline"),
        "summary": trend_summary,
        "market_pulse": pulse,
        "history_summary": {
            "record_count": history.get("record_count"),
            "trend": trend,
            "latest": history.get("latest"),
            "previous": history.get("previous"),
        },
        "driver_readout": driver_lines,
        "audience_readouts": readouts,
        "markdown": "\n".join(markdown),
    }


def provider_risk_band(score):
    score = as_float(score)
    if score >= 75:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def build_provider_risk_radar():
    comparison = read_records(DATA_DIR / "provider_comparison.csv")
    market_share = read_records(DATA_DIR / "live_provider_market_share.csv")
    health = read_records(DATA_DIR / "provider_health.csv")

    share_by_provider = {
        row.get("provider"): as_float(row.get("market_share_pct"))
        for row in market_share
    }
    health_by_provider = {
        row.get("provider"): row
        for row in health
    }

    providers = []
    for row in comparison:
        provider = row.get("provider")
        health_row = health_by_provider.get(provider, {})
        market_share_pct = share_by_provider.get(provider, 0.0)
        offers = as_float(row.get("offers"))
        gpu_types = as_float(row.get("gpu_types"))
        avg_price = as_float(row.get("avg_price"))
        health_score = as_float(health_row.get("health_score"), 50.0)
        freshness_hours = as_float(health_row.get("freshness_hours"))
        online = str(health_row.get("status", "")).lower() == "online"

        concentration_risk = clamp(market_share_pct)
        depth_risk = clamp(60.0 - min(offers, 60.0))
        diversity_risk = clamp(50.0 - min(gpu_types, 50.0))
        health_risk = clamp(100.0 - health_score)
        freshness_risk = clamp(freshness_hours / 2.0)
        price_risk = clamp(avg_price * 10.0)
        offline_risk = 25.0 if not online else 0.0

        risk_score = round(clamp(
            (concentration_risk * 0.25)
            + (depth_risk * 0.15)
            + (diversity_risk * 0.10)
            + (health_risk * 0.20)
            + (freshness_risk * 0.15)
            + (price_risk * 0.10)
            + offline_risk
        ), 2)

        if risk_score >= 75:
            action = "reduce_dependency"
        elif risk_score >= 40:
            action = "monitor_and_benchmark"
        else:
            action = "usable_benchmark"

        providers.append({
            "provider": provider,
            "risk_score": risk_score,
            "risk_band": provider_risk_band(risk_score),
            "recommended_action": action,
            "drivers": {
                "market_share_pct": market_share_pct,
                "offers": offers,
                "gpu_types": gpu_types,
                "avg_price": avg_price,
                "health_score": health_score,
                "freshness_hours": freshness_hours,
                "online": online,
            },
        })

    providers = sorted(providers, key=lambda item: item["risk_score"], reverse=True)
    highest_risk = providers[0] if providers else {}
    safest = sorted(providers, key=lambda item: item["risk_score"])[0] if providers else {}

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "provider_risk_radar",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider_count": len(providers),
        "highest_risk_provider": highest_risk,
        "lowest_risk_provider": safest,
        "providers": providers,
    }


def build_data_trust_status():
    freshness = read_records(DATA_DIR / "data_freshness.csv")
    sources = read_records(DATA_DIR / "data_source_status.csv")
    provider_mode = read_latest(DATA_DIR / "provider_data_mode.csv")
    provider_health = read_records(DATA_DIR / "provider_health.csv")

    stale_files = [
        row for row in freshness
        if not as_bool(row.get("fresh"))
    ]
    missing_files = [
        row for row in freshness
        if not as_bool(row.get("exists"))
    ]
    placeholder_sources = [
        row for row in sources
        if str(row.get("status", "")).lower() in {"placeholder", "fallback", "synthetic"}
    ]
    stale_providers = [
        row for row in provider_health
        if as_float(row.get("freshness_hours")) > 24
    ]
    offline_providers = [
        row for row in provider_health
        if str(row.get("status", "")).lower() != "online"
    ]

    live_provider_rows = as_float(provider_mode.get("live_provider_rows"))
    live_providers_configured = as_float(provider_mode.get("live_providers_configured"))

    penalties = (
        len(stale_files) * 8
        + len(missing_files) * 15
        + len(placeholder_sources) * 10
        + len(stale_providers) * 12
        + len(offline_providers) * 12
    )
    if live_providers_configured < 2:
        penalties += 12
    if live_provider_rows <= 0:
        penalties += 20

    trust_score = round(clamp(100.0 - penalties), 2)
    if trust_score >= 85:
        trust_level = "high"
    elif trust_score >= 65:
        trust_level = "medium"
    elif trust_score >= 40:
        trust_level = "low"
    else:
        trust_level = "critical"

    if trust_level in {"high", "medium"}:
        product_label = "decision_support_ready"
    elif live_provider_rows > 0:
        product_label = "beta_research_mode"
    else:
        product_label = "demo_mode"

    blockers = []
    if placeholder_sources:
        blockers.append("placeholder_sources_present")
    if stale_providers:
        blockers.append("provider_data_stale")
    if live_providers_configured < 2:
        blockers.append("provider_coverage_too_thin")
    if missing_files:
        blockers.append("freshness_files_missing")

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "data_trust_status",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "trust_score": trust_score,
        "trust_level": trust_level,
        "product_label": product_label,
        "paid_claims_allowed": trust_level in {"high", "medium"} and not placeholder_sources,
        "blockers": blockers,
        "summary": {
            "freshness_records": len(freshness),
            "stale_files": len(stale_files),
            "missing_files": len(missing_files),
            "sources": len(sources),
            "placeholder_sources": len(placeholder_sources),
            "provider_count": len(provider_health),
            "stale_providers": len(stale_providers),
            "offline_providers": len(offline_providers),
            "live_providers_configured": live_providers_configured,
            "live_provider_rows": live_provider_rows,
        },
        "freshness": freshness,
        "sources": sources,
        "provider_health": provider_health,
    }


def build_daily_change_brief():
    pulse = build_market_pulse()
    pulse_history = build_market_pulse_history()
    provider_radar = build_provider_risk_radar()
    trust = build_data_trust_status()
    signals = build_market_signals()["signals"]

    trend = pulse_history.get("trend", {})
    delta = as_float(trend.get("delta"))
    direction = trend.get("direction", "flat")
    record_count = pulse_history.get("record_count", 0)
    highest_provider = provider_radar.get("highest_risk_provider", {})
    high_signals = [
        signal for signal in signals
        if signal.get("severity") == "high"
    ]

    if record_count < 2:
        headline = "Daily change intelligence is collecting baseline history."
        change_summary = (
            "AI-RPCT has not collected enough market pulse snapshots to produce a high-conviction daily delta yet."
        )
    elif direction == "up":
        headline = "AI infrastructure pressure increased since the previous pulse."
        change_summary = f"Market Pulse moved up by {delta} points, indicating rising pressure."
    elif direction == "down":
        headline = "AI infrastructure pressure eased since the previous pulse."
        change_summary = f"Market Pulse moved down by {abs(delta)} points, indicating easing pressure."
    else:
        headline = "AI infrastructure pressure is stable versus the previous pulse."
        change_summary = "Market Pulse is flat versus the previous snapshot."

    recommended_decision = "monitor"
    if trust.get("trust_level") == "critical":
        recommended_decision = "improve_data_trust_before_paid_claims"
    elif direction == "up" and abs(delta) >= 5:
        recommended_decision = "benchmark_providers_before_capacity_commitment"
    elif highest_provider.get("risk_band") in {"medium", "high"}:
        recommended_decision = "review_provider_exposure"

    changes = [
        {
            "type": "market_pulse",
            "direction": direction,
            "delta": delta,
            "record_count": record_count,
            "latest_score": pulse.get("market_pulse_score"),
            "latest_band": pulse.get("market_pulse_band"),
        },
        {
            "type": "provider_risk",
            "direction": "watch" if highest_provider else "unknown",
            "provider": highest_provider.get("provider"),
            "risk_score": highest_provider.get("risk_score"),
            "risk_band": highest_provider.get("risk_band"),
            "recommended_action": highest_provider.get("recommended_action"),
        },
        {
            "type": "data_trust",
            "direction": "blocked" if trust.get("blockers") else "clear",
            "trust_score": trust.get("trust_score"),
            "trust_level": trust.get("trust_level"),
            "blockers": trust.get("blockers"),
        },
    ]

    if high_signals:
        changes.append({
            "type": "high_severity_signals",
            "direction": "active",
            "count": len(high_signals),
            "signals": [signal.get("title") for signal in high_signals[:5]],
        })

    markdown = [
        "# AI-RPCT Daily Change Brief",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Headline",
        headline,
        "",
        "## Change Summary",
        change_summary,
        "",
        "## Recommended Decision",
        recommended_decision,
        "",
        "## Changes",
        *[
            f"- {item.get('type')}: {item.get('direction')} "
            f"({item.get('delta', item.get('risk_score', item.get('trust_score', 'n/a')))})."
            for item in changes
        ],
        "",
        "## Trust Guardrails",
        f"- Trust Level: {trust.get('trust_level')}",
        f"- Paid Claims Allowed: {trust.get('paid_claims_allowed')}",
        f"- Blockers: {', '.join(trust.get('blockers', [])) or 'none'}",
    ]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "daily_change_brief",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "summary": change_summary,
        "recommended_decision": recommended_decision,
        "changes": changes,
        "market_pulse": pulse,
        "provider_risk": provider_radar,
        "data_trust": {
            "trust_score": trust.get("trust_score"),
            "trust_level": trust.get("trust_level"),
            "product_label": trust.get("product_label"),
            "paid_claims_allowed": trust.get("paid_claims_allowed"),
            "blockers": trust.get("blockers"),
        },
        "markdown": "\n".join(markdown),
    }


def build_trust_remediation_plan():
    trust = build_data_trust_status()
    summary = trust.get("summary", {})
    blockers = set(trust.get("blockers", []))

    actions = []
    if "placeholder_sources_present" in blockers:
        actions.append({
            "priority": "critical",
            "action": "replace_placeholder_provider_sources",
            "title": "Replace placeholder provider sources with verified live connectors",
            "rationale": "Placeholder sources prevent paid claims and weaken buyer trust.",
            "success_metric": "placeholder_sources reaches 0",
            "current_value": summary.get("placeholder_sources"),
        })

    if "provider_data_stale" in blockers:
        actions.append({
            "priority": "critical",
            "action": "restore_provider_freshness",
            "title": "Restore provider freshness below 24 hours",
            "rationale": "Stale provider data blocks decision-ready procurement claims.",
            "success_metric": "stale_providers reaches 0",
            "current_value": summary.get("stale_providers"),
        })

    if "provider_coverage_too_thin" in blockers:
        actions.append({
            "priority": "high",
            "action": "expand_live_provider_coverage",
            "title": "Expand live provider coverage beyond a single configured provider",
            "rationale": "A Bloomberg-style terminal needs enough provider breadth to compare market conditions.",
            "success_metric": "live_providers_configured >= 3",
            "current_value": summary.get("live_providers_configured"),
        })

    if "freshness_files_missing" in blockers:
        actions.append({
            "priority": "high",
            "action": "repair_freshness_inputs",
            "title": "Repair missing freshness inputs",
            "rationale": "Trust scoring depends on complete freshness telemetry.",
            "success_metric": "missing_files reaches 0",
            "current_value": summary.get("missing_files"),
        })

    if not actions:
        actions.append({
            "priority": "medium",
            "action": "maintain_trust_monitoring",
            "title": "Maintain trust monitoring cadence",
            "rationale": "Trust guardrails are currently clear. Continue collecting freshness and source provenance.",
            "success_metric": "trust_level remains medium or high",
            "current_value": trust.get("trust_level"),
        })

    critical_count = len([item for item in actions if item["priority"] == "critical"])
    high_count = len([item for item in actions if item["priority"] == "high"])

    if critical_count:
        readiness_path = "blocked_by_critical_trust_issues"
    elif high_count:
        readiness_path = "near_decision_support_ready"
    else:
        readiness_path = "maintain_and_validate"

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "trust_remediation_plan",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "readiness_path": readiness_path,
        "current_trust": {
            "trust_score": trust.get("trust_score"),
            "trust_level": trust.get("trust_level"),
            "product_label": trust.get("product_label"),
            "paid_claims_allowed": trust.get("paid_claims_allowed"),
            "blockers": trust.get("blockers"),
        },
        "action_count": len(actions),
        "actions": actions,
        "next_action": actions[0],
    }


def normalize_provider_name(name):
    normalized = str(name or "").lower().replace(".ai", "").replace(" labs", "")
    if normalized == "lambda":
        return "lambda"
    if normalized == "vast":
        return "vast"
    return normalized.replace(" ", "_")


def build_provider_connector_readiness():
    sources = read_records(DATA_DIR / "data_source_status.csv")
    credentials = read_records(DATA_DIR / "provider_credentials.csv")
    provider_health = read_records(DATA_DIR / "provider_health.csv")
    comparison = read_records(DATA_DIR / "provider_comparison.csv")

    credentials_by_provider = {
        normalize_provider_name(row.get("provider")): as_bool(row.get("configured"))
        for row in credentials
    }
    health_by_provider = {
        normalize_provider_name(row.get("provider")): row
        for row in provider_health
    }
    comparison_by_provider = {
        normalize_provider_name(row.get("provider")): row
        for row in comparison
    }

    provider_sources = [
        row for row in sources
        if str(row.get("type", "")).lower() == "gpu_provider"
    ]

    providers = []
    for source in provider_sources:
        provider_key = normalize_provider_name(source.get("source"))
        source_status = str(source.get("status", "")).lower()
        health = health_by_provider.get(provider_key, {})
        comparison_row = comparison_by_provider.get(provider_key, {})
        credential_configured = credentials_by_provider.get(provider_key, False)
        freshness_hours = as_float(health.get("freshness_hours"), 999.0)
        live_rows = as_float(health.get("rows"))
        offers = as_float(comparison_row.get("offers"))

        if source_status == "live_external" and freshness_hours <= 24 and live_rows > 0:
            readiness = "verified_live"
            next_action = "maintain_connector"
        elif source_status == "placeholder" and live_rows > 0:
            readiness = "placeholder_with_rows"
            next_action = "verify_or_replace_source_provenance"
        elif live_rows > 0 and freshness_hours <= 24:
            readiness = "live_unverified"
            next_action = "verify_source_status"
        elif live_rows > 0:
            readiness = "stale_live_data"
            next_action = "refresh_provider_collection"
        elif credential_configured:
            readiness = "credentials_configured_no_rows"
            next_action = "debug_connector_ingestion"
        else:
            readiness = "placeholder"
            next_action = "configure_or_replace_connector"

        providers.append({
            "provider": provider_key,
            "source": source.get("source"),
            "source_status": source_status,
            "credential_configured": credential_configured,
            "readiness": readiness,
            "next_action": next_action,
            "freshness_hours": freshness_hours,
            "rows": live_rows,
            "offers": offers,
        })

    readiness_counts = {}
    for provider in providers:
        readiness = provider["readiness"]
        readiness_counts[readiness] = readiness_counts.get(readiness, 0) + 1

    blockers = [
        provider for provider in providers
        if provider["readiness"] != "verified_live"
    ]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "provider_connector_readiness",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider_count": len(providers),
        "verified_live_count": readiness_counts.get("verified_live", 0),
        "readiness_counts": readiness_counts,
        "connector_blockers": len(blockers),
        "providers": providers,
        "next_provider_action": blockers[0] if blockers else {},
    }


def connector_upgrade_priority(provider):
    readiness = provider.get("readiness")
    freshness_hours = as_float(provider.get("freshness_hours"), 999.0)
    offers = as_float(provider.get("offers"))
    rows = as_float(provider.get("rows"))

    readiness_weight = {
        "placeholder": 88.0,
        "placeholder_with_rows": 82.0,
        "stale_live_data": 72.0,
        "credentials_configured_no_rows": 66.0,
        "live_unverified": 48.0,
        "verified_live": 0.0,
    }.get(readiness, 60.0)

    coverage_weight = min(offers, 100.0) * 0.08
    freshness_weight = min(freshness_hours, 168.0) * 0.04
    missing_rows_weight = 8.0 if rows <= 0 else 0.0

    return round(clamp(readiness_weight + coverage_weight + freshness_weight + missing_rows_weight), 2)


def connector_upgrade_steps(provider):
    readiness = provider.get("readiness")
    source = provider.get("source") or provider.get("provider")

    if readiness == "placeholder":
        return [
            f"Select verified source strategy for {source}.",
            "Configure provider credential or replace placeholder feed with a documented public connector.",
            "Run provider collection and write source provenance into data_source_status.csv.",
            "Validate rows, freshness below 24 hours and provider_health coverage.",
        ]
    if readiness == "placeholder_with_rows":
        return [
            f"Verify source provenance for {source}.",
            "Replace placeholder source label with documented live evidence only after reproducible collection is confirmed.",
            "Refresh provider collection and confirm freshness below 24 hours.",
            "Update data_source_status.csv and provider_health telemetry together.",
        ]
    if readiness == "stale_live_data":
        return [
            f"Refresh {source} provider collection.",
            "Verify scheduler cadence and ingestion logs.",
            "Confirm freshness_hours drops below 24.",
        ]
    if readiness == "credentials_configured_no_rows":
        return [
            f"Debug {source} connector ingestion with existing credentials.",
            "Check authentication, rate limits and response parsing.",
            "Persist first valid rows and update provider health telemetry.",
        ]
    if readiness == "live_unverified":
        return [
            f"Verify {source} source label and provenance.",
            "Mark source as live_external only after reproducible collection evidence exists.",
            "Retain audit notes for buyer-facing trust claims.",
        ]
    return [
        f"Keep {source} connector monitored.",
        "Maintain freshness below 24 hours and source provenance.",
    ]


def build_provider_connector_upgrade_plan():
    readiness = build_provider_connector_readiness()
    trust = build_data_trust_status()
    providers = []

    for provider in readiness.get("providers", []):
        priority_score = connector_upgrade_priority(provider)
        if provider.get("readiness") == "verified_live":
            impact = "maintenance"
            buyer_value = "Preserves existing buyer confidence."
        elif provider.get("readiness") in {"placeholder", "placeholder_with_rows"}:
            impact = "critical_trust_unlock"
            buyer_value = "Replaces demo-mode evidence with source-backed provider intelligence."
        elif provider.get("readiness") == "stale_live_data":
            impact = "freshness_unlock"
            buyer_value = "Restores decision confidence for provider comparison and risk scoring."
        else:
            impact = "source_confidence_unlock"
            buyer_value = "Improves provenance and reduces ambiguity in provider claims."

        providers.append({
            **provider,
            "priority_score": priority_score,
            "impact": impact,
            "buyer_value": buyer_value,
            "upgrade_steps": connector_upgrade_steps(provider),
            "success_metric": "readiness becomes verified_live",
        })

    providers = sorted(providers, key=lambda item: item["priority_score"], reverse=True)
    blocking = [provider for provider in providers if provider.get("readiness") != "verified_live"]

    if not blocking:
        headline = "Provider connector layer is ready for trust-maintenance mode."
        rollout_phase = "maintain_verified_connectors"
    elif trust.get("paid_claims_allowed"):
        headline = "Connector upgrades can deepen the moat while paid claims remain allowed."
        rollout_phase = "expand_data_moat"
    else:
        headline = "Connector upgrades are the fastest path to unlock paid trust claims."
        rollout_phase = "clear_trust_blockers"

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "provider_connector_upgrade_plan",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "rollout_phase": rollout_phase,
        "provider_count": readiness.get("provider_count", 0),
        "blocking_provider_count": len(blocking),
        "verified_live_count": readiness.get("verified_live_count", 0),
        "current_trust": {
            "trust_score": trust.get("trust_score"),
            "trust_level": trust.get("trust_level"),
            "paid_claims_allowed": trust.get("paid_claims_allowed"),
            "blockers": trust.get("blockers"),
        },
        "next_upgrade": blocking[0] if blocking else providers[0] if providers else {},
        "providers": providers,
    }


def save_market_pulse_brief():
    REPORTS_DIR.mkdir(exist_ok=True)
    brief = build_market_pulse_brief()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    path = REPORTS_DIR / f"market_pulse_brief_{stamp}.md"
    path.write_text(brief["markdown"])
    return {
        "status": "saved",
        "file": str(path),
        "report_type": brief["report_type"],
        "headline": brief["headline"],
    }


def build_recommendations():
    signals = build_market_signals()["signals"]
    terminal = read_latest(DATA_DIR / "terminal_summary.csv")
    provider_comparison = read_records(DATA_DIR / "provider_comparison.csv")
    provider_health = read_records(DATA_DIR / "provider_health.csv")
    cheapest = read_records(DATA_DIR / "live_gpu_cheapest.csv")
    scarcity = read_records(DATA_DIR / "scarcity_watchlist.csv")

    recommendations = []
    signal_types = {signal.get("type") for signal in signals}
    risk_signal = next((signal for signal in signals if signal.get("type") == "risk"), {})

    online_providers = {
        row.get("provider")
        for row in provider_health
        if row.get("status") == "online"
    }
    ranked_providers = sorted(
        provider_comparison,
        key=lambda row: (
            0 if row.get("provider") in online_providers else 1,
            -as_float(row.get("offers")),
            as_float(row.get("avg_price"), 999999)
        )
    )

    if ranked_providers:
        provider = ranked_providers[0]
        recommendations.append({
            "action": "primary_provider_watch",
            "priority": "high" if risk_signal.get("severity") == "high" else "medium",
            "title": f"Use {provider.get('provider')} as the primary provider benchmark",
            "rationale": "This provider has the strongest current combination of online status and tracked offer depth.",
            "evidence": {
                "provider": provider.get("provider"),
                "offers": provider.get("offers"),
                "gpu_types": provider.get("gpu_types"),
                "avg_price": provider.get("avg_price")
            }
        })

    if "opportunity" in signal_types and cheapest:
        gpu = cheapest[0]
        recommendations.append({
            "action": "evaluate_buy_window",
            "priority": "high",
            "title": f"Evaluate short-term buying window for {gpu.get('gpu')}",
            "rationale": "Price pressure is easing and a low-cost GPU candidate is visible in the live market.",
            "evidence": {
                "gpu": gpu.get("gpu"),
                "avg_price": gpu.get("avg_price"),
                "min_price": gpu.get("min_price"),
                "offers": gpu.get("offers")
            }
        })
    elif cheapest:
        gpu = cheapest[0]
        recommendations.append({
            "action": "track_low_cost_capacity",
            "priority": "medium",
            "title": f"Track low-cost capacity around {gpu.get('gpu')}",
            "rationale": "This is currently the lowest-cost tracked GPU and can anchor budget-sensitive workloads.",
            "evidence": {
                "gpu": gpu.get("gpu"),
                "avg_price": gpu.get("avg_price"),
                "min_price": gpu.get("min_price"),
                "offers": gpu.get("offers")
            }
        })

    scarce_frontier = [
        row for row in scarcity
        if str(row.get("category", "")).lower() == "frontier"
        and str(row.get("scarcity_flag", "")).lower() == "true"
    ]
    if scarce_frontier:
        recommendations.append({
            "action": "protect_frontier_capacity",
            "priority": "high",
            "title": "Protect frontier GPU capacity decisions",
            "rationale": "Frontier GPU scarcity is visible. Avoid relying on a single provider or a single GPU type.",
            "evidence": {
                "scarce_gpus": [row.get("gpu") for row in scarce_frontier[:5]],
                "count": len(scarce_frontier)
            }
        })

    risk_score = as_float(read_latest(DATA_DIR / "terminal_risk_score.csv").get("terminal_risk_score"))
    if risk_score >= 80:
        recommendations.append({
            "action": "escalate_risk_review",
            "priority": "high",
            "title": "Escalate infrastructure risk review",
            "rationale": "Risk is high enough to justify reviewing provider exposure, capacity timing and budget assumptions.",
            "evidence": {"terminal_risk_score": risk_score}
        })
    elif risk_score >= 60:
        recommendations.append({
            "action": "maintain_watch_mode",
            "priority": "medium",
            "title": "Maintain watch mode",
            "rationale": "Risk is elevated but not extreme. Keep monitoring before making irreversible commitments.",
            "evidence": {"terminal_risk_score": risk_score}
        })

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "market_context": {
            "top_provider": terminal.get("top_provider"),
            "gpu_price_trend": terminal.get("gpu_price_trend"),
            "active_alerts": terminal.get("active_alerts")
        },
        "recommendations": recommendations,
        "recommendation_count": len(recommendations)
    }


def build_executive_brief():
    summary = build_terminal_summary()
    signals = build_market_signals()["signals"]
    recommendations = build_recommendations()["recommendations"]

    terminal = summary.get("terminal", {})
    risk = summary.get("risk", {})
    quality = summary.get("quality", {})
    scarcity = summary.get("scarcity", {})
    frontier = summary.get("frontier", {})

    high_priority = [
        item for item in recommendations
        if item.get("priority") == "high"
    ]
    top_recommendations = high_priority[:3] or recommendations[:3]
    top_signals = signals[:5]

    risk_level = risk.get("risk_level", "unknown")
    risk_score = risk.get("terminal_risk_score", "n/a")
    ai_index = terminal.get("ai_infrastructure_index", "n/a")
    gpu_price_index = terminal.get("gpu_price_index", "n/a")
    trend = terminal.get("gpu_price_trend", "unknown")
    top_provider = terminal.get("top_provider", "unknown")

    if risk_level == "high" or as_float(risk_score) >= 75:
        headline = "AI infrastructure risk remains elevated."
        summary_text = (
            "The terminal is showing elevated infrastructure risk, with frontier GPU scarcity "
            "and provider concentration requiring active monitoring."
        )
    elif trend and trend != "stable":
        headline = "GPU market conditions are moving."
        summary_text = (
            "The latest terminal snapshot shows a directional GPU pricing signal. "
            "Buyers should compare provider depth before committing capacity."
        )
    else:
        headline = "AI infrastructure conditions are stable but watchlisted."
        summary_text = (
            "The latest terminal snapshot is stable overall, while selected GPU categories "
            "and provider exposure still deserve monitoring."
        )

    markdown = [
        "# AI-RPCT Executive Brief",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"## Headline",
        headline,
        "",
        "## Market Summary",
        summary_text,
        "",
        "## Core Metrics",
        f"- AI Infrastructure Index: {ai_index}",
        f"- GPU Price Index: {gpu_price_index}",
        f"- GPU Price Trend: {trend}",
        f"- Terminal Risk Score: {risk_score}",
        f"- Risk Level: {risk_level}",
        f"- Top Provider: {top_provider}",
        f"- Live Data Quality: {quality.get('live_data_quality_score', 'n/a')}",
        f"- GPU Scarcity Index: {scarcity.get('gpu_scarcity_index', 'n/a')}",
        f"- Frontier GPU Index: {frontier.get('frontier_gpu_index', 'n/a')}",
        "",
        "## Top Signals",
        *[f"- {item.get('severity', 'n/a').upper()}: {item.get('title', '')}" for item in top_signals],
        "",
        "## Recommended Actions",
        *[f"- {item.get('priority', 'n/a').upper()}: {item.get('title', '')}" for item in top_recommendations],
    ]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "report_type": "executive_brief",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "summary": summary_text,
        "core_metrics": {
            "ai_infrastructure_index": ai_index,
            "gpu_price_index": gpu_price_index,
            "gpu_price_trend": trend,
            "terminal_risk_score": risk_score,
            "risk_level": risk_level,
            "top_provider": top_provider,
            "live_data_quality_score": quality.get("live_data_quality_score"),
            "gpu_scarcity_index": scarcity.get("gpu_scarcity_index"),
            "frontier_gpu_index": frontier.get("frontier_gpu_index")
        },
        "top_signals": top_signals,
        "recommended_actions": top_recommendations,
        "markdown": "\n".join(markdown)
    }


def build_terminal_summary():
    terminal = read_latest(DATA_DIR / "terminal_summary.csv")
    risk = read_latest(DATA_DIR / "terminal_risk_score.csv")
    quality = read_latest(DATA_DIR / "live_data_quality_score.csv")
    pulse = read_latest(DATA_DIR / "ai_infrastructure_pulse.csv")
    scarcity = read_latest(DATA_DIR / "gpu_scarcity_index.csv")
    frontier = read_latest(DATA_DIR / "frontier_gpu_index.csv")

    return {
        "product": "AI-RPCT",
        "mission": "Bloomberg for AI Infrastructure",
        "status": "ok" if terminal else "degraded",
        "terminal": terminal,
        "risk": risk,
        "quality": quality,
        "pulse": pulse,
        "scarcity": scarcity,
        "frontier": frontier
    }


def build_dashboard_snapshot():
    return {
        **build_terminal_summary(),
        "signals": build_market_signals()["signals"],
        "recommendations": [],
        "executive_brief": {
            "headline": "Executive brief requires Pro access",
            "summary": "Add a Pro or Enterprise API key in the terminal to unlock recommendations and executive reporting."
        },
        "market_share": read_records(DATA_DIR / "live_provider_market_share.csv"),
        "provider_health": read_records(DATA_DIR / "provider_health.csv"),
        "provider_comparison": read_records(DATA_DIR / "provider_comparison.csv"),
        "gpu_rankings": read_records(DATA_DIR / "live_gpu_most_expensive.csv")[:10],
        "gpu_watchlist": read_records(DATA_DIR / "gpu_watchlist_intelligence.csv"),
        "alerts": read_records(DATA_DIR / "live_gpu_alerts.csv")
    }


def build_api_catalog():
    catalog = read_records(DATA_DIR / "api_catalog.csv")
    core_endpoints = [
        {
            "endpoint": "/v1/terminal-summary",
            "category": "core",
            "description": "Stable AI-RPCT terminal summary.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/dashboard-snapshot",
            "category": "core",
            "description": "Stable dashboard payload for the web terminal.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/data-trust-status",
            "category": "trust",
            "description": "Public data trust status with freshness, source labels, blockers and paid-claims guardrails.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/trust-remediation-plan",
            "category": "trust",
            "description": "Prioritized action plan for clearing trust blockers and reaching paid-claims readiness.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/provider-connector-readiness",
            "category": "trust",
            "description": "Provider connector readiness matrix with source labels, credentials, freshness and next integration action.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/provider-connector-upgrade-plan",
            "category": "trust",
            "description": "Prioritized provider connector upgrade workflow with implementation steps, trust impact and next best provider fix.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/market-pulse",
            "category": "intelligence",
            "description": "Proprietary AI infrastructure market pulse with pressure, confidence and audience readouts.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/market-pulse-history",
            "category": "intelligence",
            "description": "Historical AI infrastructure market pulse with latest delta and direction.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/market-pulse/snapshot",
            "category": "intelligence",
            "description": "Persist the current proprietary market pulse into the historical data moat.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/market-pulse-brief",
            "category": "reports",
            "description": "Executive-readable market pulse brief with trend summary, drivers and audience readouts.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/market-pulse-brief/save",
            "category": "reports",
            "description": "Persist the current market pulse brief as a markdown report artifact.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/provider-risk-radar",
            "category": "intelligence",
            "description": "Provider risk radar scoring concentration, depth, diversity, freshness, health and price exposure.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/daily-change-brief",
            "category": "intelligence",
            "description": "Daily change intelligence summarizing market pulse movement, provider risk and trust blockers.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/reports/latest",
            "category": "reports",
            "description": "Latest generated intelligence reports.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/access-status",
            "category": "access",
            "description": "Current API key plan, allowed endpoints and recent usage status.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/plan-limits",
            "category": "access",
            "description": "Published request limits for Free, Pro and Enterprise plans.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/usage-summary",
            "category": "access",
            "description": "Usage summary for the current API key.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/commercial-snapshot",
            "category": "commercial",
            "description": "Enterprise commercial dashboard with accounts, usage, limits, MRR and upgrade signals.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/sales-pipeline",
            "category": "commercial",
            "description": "Enterprise sales pipeline generated from usage, limits and account upgrade signals.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customer-admin",
            "category": "commercial",
            "description": "Enterprise customer administration snapshot with account status, plan, usage and limits.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/account-health",
            "category": "commercial",
            "description": "Enterprise account health scoring for retention, adoption and expansion operations.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/revenue-forecast",
            "category": "commercial",
            "description": "Enterprise revenue forecast combining current MRR, pipeline lift and account health risk.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/commercial-board-report",
            "category": "reports",
            "description": "Enterprise commercial board report payload with revenue, pipeline and account health.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/commercial-board-report/html",
            "category": "reports",
            "description": "PDF-ready HTML version of the enterprise commercial board report.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/audit-log",
            "category": "commercial",
            "description": "Enterprise audit trail for customer and API-key administration actions.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/operations-status",
            "category": "operations",
            "description": "Enterprise operational readiness status for V1 API, data, monetization and commercial launch.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/launch-controls",
            "category": "operations",
            "description": "Enterprise launch-control flags for billing, terms, paid onboarding and public demo status.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customers",
            "category": "commercial",
            "description": "Enterprise customer onboarding endpoint that creates an account and active V1 API key.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customers/revoke",
            "category": "commercial",
            "description": "Enterprise customer lifecycle endpoint that revokes a V1 API key.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customers/reactivate",
            "category": "commercial",
            "description": "Enterprise customer lifecycle endpoint that reactivates a revoked V1 API key.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/signals",
            "category": "intelligence",
            "description": "Decision signals generated from live market, price, scarcity and provider data.",
            "tier": "free"
        },
        {
            "endpoint": "/v1/recommendations",
            "category": "intelligence",
            "description": "Actionable AI infrastructure recommendations generated from terminal signals.",
            "tier": "pro"
        },
        {
            "endpoint": "/v1/executive-brief",
            "category": "reports",
            "description": "Executive-ready market brief generated from terminal metrics, signals and recommendations.",
            "tier": "enterprise"
        },
        {
            "endpoint": "/v1/customer-report",
            "category": "reports",
            "description": "PDF-ready customer intelligence report payload with markdown and HTML export support.",
            "tier": "enterprise"
        }
    ]

    return {
        "product": "AI-RPCT",
        "version": "v1",
        "core_endpoints": core_endpoints,
        "legacy_catalog": catalog
    }


def build_latest_reports():
    return {
        "daily_terminal_brief": read_latest_report("daily_terminal_brief_*.txt"),
        "weekly_infrastructure_report": read_latest_report("weekly_infrastructure_report_*.txt"),
        "market_intelligence_snapshot": read_latest_report("market_intelligence_snapshot_*.txt"),
        "executive_ai_memo": read_latest_report("executive_ai_infrastructure_memo_*.txt"),
        "investor_snapshot": read_latest_report("investor_snapshot_*.txt")
    }
