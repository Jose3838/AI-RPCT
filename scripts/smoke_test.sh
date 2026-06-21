#!/usr/bin/env bash
set -euo pipefail
BASE=${BASE_URL:-http://127.0.0.1:8000}

echo "Checking ${BASE}/health ..."
HTTP=$(curl -s -o /dev/null -w "%{http_code}" ${BASE}/health)
if [ "$HTTP" -ne 200 ]; then
  echo "Health check failed: HTTP $HTTP"; exit 2
fi

echo "Checking ${BASE}/dashboard-metrics ..."
HTTP=$(curl -s -o /dev/null -w "%{http_code}" ${BASE}/dashboard-metrics)
if [ "$HTTP" -ne 200 ]; then
  echo "Dashboard metrics check failed: HTTP $HTTP"; exit 3
fi

echo "Smoke tests passed."
