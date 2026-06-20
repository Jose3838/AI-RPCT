# AI-RPCT Runbook V1

## 1. Projektstatus prüfen

git status
git branch --show-current
git log --oneline -10

## 2. Hourly Collection manuell ausführen

./run_hourly_collection.sh

## 3. LaunchAgent prüfen

launchctl list | grep com.airpct.hourly.collection
cat ~/Library/LaunchAgents/com.airpct.hourly.collection.plist

## 4. Collection Health prüfen

python - <<'PY'
from main import terminal_collection_health_v2
import json

print(json.dumps(
    terminal_collection_health_v2(),
    indent=2
))
PY

## 5. Strategy Dashboard prüfen

python - <<'PY'
from main import terminal_strategy_dashboard_v1
import json

print(json.dumps(
    terminal_strategy_dashboard_v1(),
    indent=2,
    default=str
))
PY

## 6. Intelligence Summary V2

python - <<'PY'
from main import terminal_intelligence_summary_v2
import json

print(json.dumps(
    terminal_intelligence_summary_v2(),
    indent=2,
    default=str
))
PY

## 7. Lokale API starten

uvicorn main:app --reload

## 8. Wichtigste Endpoints

/terminal-intelligence-summary-v2
/terminal-strategy-dashboard-v1
/terminal-product-readiness-v1
/terminal-executive-scorecard-v1
/terminal-investor-readiness-v1
/terminal-data-moat-v2
/terminal-forecast-accuracy-trend-v1
/terminal-collection-health-v2
/terminal-launchagent-health-v1
