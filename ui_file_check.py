from pathlib import Path

required = {
    "web/index.html": [
        "AI-RPCT Command Terminal",
        "execObservations",
        "marketRegime",
        "liveCoverage",
        "forecastSignal",
        "systemHealthStrip",
        "signalTape",
        "moatReadout",
        "forecastReadinessScore",
        "gpuMarketDepthTable",
        "gpuGainersTable",
        "gpuLosersTable",
        "coverageActionPlanTable",
    ],
    "web/app.js": [
        "renderExecutiveSummary",
        "renderFinalWidgets",
        "renderSystemHealthStrip",
        "renderSignalTape",
        "renderDataMoatPanel",
        "renderForecastReadiness",
        "renderMarketMovers",
    ],
    "web/terminal.css": [
        ".executive-strip",
        ".hero",
        ".card",
        ".signal-tape",
        ".health-strip",
        ".moat-card",
        ".forecast-card",
        ".regime-card",
        ".coverage-card",
        ".forecast-signal-card",
        ".coverage-action-card",
    ],
}

failed = []

for file, needles in required.items():
    text = Path(file).read_text()
    for needle in needles:
        if needle not in text:
            failed.append((file, needle))

if failed:
    print("Missing UI markers:")
    for file, needle in failed:
        print(file, needle)
    raise SystemExit(1)

print("UI FILE CHECK PASSED")
