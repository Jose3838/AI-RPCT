# Registry Schema Framework v1

## Purpose

This module introduces machine-readable registry schemas for AI-RPCT.

Schemas define required columns, unique identifiers, governed values, and cross-registry references.

## Initial Schema

- historical_capacity_registry.schema.json

## Governance

Rules:

- schemas validate structure before future downstream use
- schema validation does not generate facts
- schema validation does not infer missing data
- schema validation does not add prices, capacity claims, or labels

## Changelog

### v1

Initial schema framework with historical capacity registry schema validation.
