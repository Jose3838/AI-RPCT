#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=============================="
echo "AI-RPCT HOURLY COLLECTION"
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "=============================="

if [ -d "venv" ]; then
  source venv/bin/activate
fi

python - <<'PY'
from intelligence.master_intelligence_collector import (
    run_master_intelligence_collector
)

import json

result = run_master_intelligence_collector()

print(json.dumps(result, indent=2, default=str))

required_keys = [
    "gpu_state",
    "providers",
    "forecast",
    "coverage",
]

missing = [
    key for key in required_keys
    if key not in result
]

if missing:
    raise SystemExit(
        f"Hourly collection incomplete. Missing keys: {missing}"
    )

provider_saved = result.get("providers", {}).get("saved", 0)
forecast_saved = result.get("forecast", {}).get("saved", 0)

if provider_saved <= 0:
    raise SystemExit("Hourly collection failed: no provider rows saved")

if forecast_saved <= 0:
    raise SystemExit("Hourly collection failed: no forecast rows saved")
PY

echo ""
echo "Hourly collection completed successfully"
echo ""
