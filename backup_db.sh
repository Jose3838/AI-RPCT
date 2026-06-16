#!/bin/bash
cd ~/AI-RPCT
mkdir -p backups
DATE=$(date +%Y%m%d_%H%M%S)
cp data/airpct.db backups/airpct_$DATE.db
echo "Database backup created: backups/airpct_$DATE.db"
