#!/bin/bash
set -euo pipefail

LABEL="com.airpct.daily"
USER_DOMAIN="gui/$(id -u)"

if launchctl print "$USER_DOMAIN/$LABEL" >/tmp/airpct_launch_agent_status.txt 2>/tmp/airpct_launch_agent_status.err; then
  echo "status=loaded"
  cat /tmp/airpct_launch_agent_status.txt
else
  echo "status=not_loaded"
  cat /tmp/airpct_launch_agent_status.err
  exit 1
fi
