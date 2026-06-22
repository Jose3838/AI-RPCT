#!/bin/bash
cd ~/AI-RPCT
source venv/bin/activate
PYTHONPATH=. pytest tests
