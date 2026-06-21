#!/usr/bin/env bash
set -euo pipefail

# CI smoke test for AI-RPCT basic endpoints and PDF export
ROOT="http://127.0.0.1:8000"
API_KEY="${AI_RPCT_API_KEY:-demo-key}"

echo "Checking root..."
curl -fsS ${ROOT}/ || { echo "Root unreachable"; exit 2; }

echo "Checking web UI..."
curl -fsS ${ROOT}/web/ > /dev/null || { echo "Web UI not reachable"; exit 2; }

echo "Checking dashboard redirect..."
curl -fsS -o /dev/null -w "%{http_code}" ${ROOT}/dashboard | grep -q "307" || { echo "Dashboard redirect failed"; exit 2; }

# Trigger PDF-ready and export
echo "Trigger PDF-ready..."
curl -fsS -H "X-API-KEY: ${API_KEY}" ${ROOT}/terminal-customer-report-pdf-ready-v1 || { echo "PDF-ready endpoint failed"; exit 2; }

echo "Trigger PDF export..."
EXPOUT=$(curl -fsS -H "X-API-KEY: ${API_KEY}" ${ROOT}/terminal-customer-report-pdf-export-v1)
if echo "$EXPOUT" | grep -q 'saved'; then
  echo "Export reported saved. Proceed to download..."
  curl -fsS -H "X-API-KEY: ${API_KEY}" -o /tmp/customer_report.pdf ${ROOT}/download/customer-report
  if [ -s /tmp/customer_report.pdf ]; then
    echo "Downloaded PDF ok: /tmp/customer_report.pdf"
  else
    echo "Downloaded PDF empty or missing"; exit 2
  fi
else
  echo "Export response did not report saved: $EXPOUT"; exit 2
fi

echo "CI smoke test passed."