# Forecast Engine v1

## Purpose

Forecast Engine v1 introduces a rule-based, non-production forecast prototype for AI-RPCT.

It is designed to validate the forecast pipeline structure without making ML claims.

## Input

data/forecast_dataset.csv

## Output

data/forecast_engine_v1_output.csv

warehouse/forecast/forecast_engine_v1_output.csv

## Governance

Forecast Engine v1 is not an ML model.

It does not use:

- true future outcome labels
- supervised learning
- model training
- benchmark evaluation
- accuracy reporting

## Allowed Usage

- pipeline validation
- dashboard prototyping
- governance testing
- rule-based monitoring experiments

## Blocked Usage

- paid production
- ML promotion
- accuracy claims
- customer-facing performance claims
- automated production decisions

## Changelog

### v1

Initial rule-based non-production forecast prototype.
