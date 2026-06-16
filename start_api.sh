#!/bin/bash
cd ~/AI-RPCT
source venv/bin/activate
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
