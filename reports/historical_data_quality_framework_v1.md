# Historical Data Quality Framework v1

## Purpose

This module introduces reusable data quality validation for AI-RPCT historical datasets.

It reduces duplicated registry-specific validation logic and creates a shared governance layer for current and future historical registries.

## Files

analytics/historical_data_quality.py
analytics/validate_registry.py
tests/test_historical_data_quality.py
reports/historical_data_quality_framework_v1.md

## Validation Rules

Initial reusable checks:

- dataset is not empty
- required columns exist
- unique identifiers are unique
- allowed values are governed
- HTTPS fields use HTTPS URLs
- duplicate rows are rejected
- reference values can be validated against known registries

## Initial Integration

The generic validator initially covers:

- Historical Source Registry
- Historical Entity Registry

Future versions should extend validation coverage to:

- AMD Historical GPU Registry
- Intel Historical GPU Registry
- Historical Relationship Registry
- CUDA Timeline
- ROCm Timeline
- Gaudi Timeline
- Provider Registry v2

## Governance

This framework does not generate facts, prices, benchmarks, forecasts, or labels.

It validates structure, consistency, and governed values only.

## Changelog

### v1

Initial reusable data quality validation framework.
