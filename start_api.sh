#!/bin/bash
cd ~/AI-RPCT 2>/dev/null || cd /app
source venv/bin/activate 2>/dev/null || true

python database/init_db.py
python database/import_csv.py

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
