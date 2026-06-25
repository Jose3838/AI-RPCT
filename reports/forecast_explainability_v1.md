# Forecast Explainability v1

## Purpose

This module adds rule-based explanations for Forecast Engine v1 outputs.

It provides transparent reasoning for monitoring signals without using ML inference.

## Input

data/forecast_engine_v1_output.csv

## Output

data/forecast_explanations.csv

warehouse/forecast/forecast_explanations.csv

## Governance

Rules:

- no ML inference
- no accuracy claims
- no production promotion
- no customer-facing performance claims
- explanations are rule-based only

## Changelog

### v1

Initial rule-based forecast explanations.
