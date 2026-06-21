# AI-RPCT Demo Guide

## Start

uvicorn main:app --reload

## Core Endpoints

### Intelligence Summary

/terminal-intelligence-summary-v2

Shows:

- System health
- Collection health
- Data moat
- Executive score
- Product readiness

### CEO Command Center

/terminal-ceo-command-center-v1

Shows:

- Customer value
- Budget advisor
- Provider switching
- GPU risk
- Customer decision center
- Demo snapshot

### Customer Decision Center

/terminal-customer-decision-center-v1

Answers:

- What to buy?
- What to avoid?
- Should I switch provider?

### Daily Intelligence Brief

/terminal-daily-intelligence-brief-v1

Daily customer briefing.

### Weekly Market Report

/terminal-weekly-market-report-v1

Weekly market overview.

### Customer PDF Report

/terminal-customer-report-pdf-export-v1

Exports:

data/reports/customer_report_v1.pdf

## Historical Assets

Key datasets:

data/live_offers/provider_live_offer_history.csv

data/forecast_audit_history.csv

data/forecast_accuracy_history.csv

data/provider_market_share_history.csv

data/feature_store/gpu_market_depth_history.csv
