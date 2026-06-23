#!/bin/bash
set -euo pipefail

LABEL="com.airpct.daily"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$PLIST_DIR/$LABEL.plist"
LOG_DIR="$REPO_DIR/logs"
USER_DOMAIN="gui/$(id -u)"

mkdir -p "$PLIST_DIR" "$LOG_DIR"

cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>cd "$REPO_DIR" &amp;&amp; ./scripts/run_core_intelligence.sh</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$REPO_DIR</string>

  <key>RunAtLoad</key>
  <true/>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>8</integer>
    <key>Minute</key>
    <integer>15</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>$LOG_DIR/launchd.daily.out.log</string>

  <key>StandardErrorPath</key>
  <string>$LOG_DIR/launchd.daily.err.log</string>
</dict>
</plist>
PLIST

chmod 644 "$PLIST_PATH"

launchctl bootout "$USER_DOMAIN" "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl bootstrap "$USER_DOMAIN" "$PLIST_PATH"
launchctl enable "$USER_DOMAIN/$LABEL"

echo "Installed $LABEL"
echo "Schedule: login plus every day at 08:15 local time"
echo "Plist: $PLIST_PATH"
echo "Logs: $LOG_DIR/launchd.daily.out.log and $LOG_DIR/launchd.daily.err.log"
echo "Status: launchctl print $USER_DOMAIN/$LABEL"
