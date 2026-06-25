# DuckDB Analytics Layer v1

## Purpose

This module creates a local DuckDB analytics database from governed AI-RPCT CSV datasets.

It enables SQL-based analysis across feature, forecast, provider, capacity, relationship, and accelerator datasets.

## Output

warehouse/analytics/ai_rpct.duckdb

## Tables

- feature_store
- forecast_dataset
- forecast_engine_v1_output
- forecast_explanations
- historical_capacity_registry
- provider_entity_registry
- provider_relationship_registry
- unified_accelerator_registry

## Governance

This layer does not create new facts, labels, prices, or forecasts.

It only loads governed CSV outputs into an analytical database.

## Changelog

### v1

Initial DuckDB analytics layer.
