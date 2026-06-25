# Forecast Dataset v1

## Purpose

This dataset introduces the first forecast-ready dataset layer for AI-RPCT.

It converts governed feature-store records into a structured dataset for future forecasting, analytics, and ML workflows.

## Dataset

Primary dataset: data/forecast_dataset.csv

Warehouse copy: warehouse/forecast/forecast_dataset.csv

## Current Fields

- forecast_record_id
- feature_id
- provider_id
- entity_id
- vendor
- architecture
- software_stack
- capacity_status
- availability_level

## Governance

Rules:

- no synthetic labels
- no invented forecast outcomes
- no accuracy claims
- no ML promotion
- no paid production enablement
- dataset is feature-only in v1

## Changelog

### v1

Initial forecast-ready dataset generated from feature-store-style records.
