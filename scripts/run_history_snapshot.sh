#!/bin/bash

cd /app || exit 1

python jobs/history_snapshot.py
