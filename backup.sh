#!/bin/bash
cd ~/AI-RPCT
mkdir -p backups
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backups/ai_rpct_backup_$DATE.tar.gz data reports *.py collectors engine analytics dashboard api config.py README.md requirements.txt requirements-lock.txt run_daily.sh start_api.sh 2>/dev/null
echo "Backup created: backups/ai_rpct_backup_$DATE.tar.gz"
