# Unified Hardware Registry v1

## Purpose

This registry introduces a canonical hardware layer for AI-RPCT.

It provides a unified view across vendor-specific historical hardware registries such as AMD, Intel, and future NVIDIA records.

## Dataset

Primary dataset: data/unified_hardware_registry.csv

Warehouse copy: warehouse/historical/metadata/unified_hardware_registry.csv

## Scope

Initial coverage:

- AMD Instinct MI100
- AMD Instinct MI300X
- Intel Data Center GPU Max 1100
- Intel Gaudi2
- Intel Gaudi3

## Governance

Rules:

- every hardware record has a stable hardware_id
- every hardware record links to an entity_id
- every hardware record links to a source_id
- source_id must exist in the Historical Source Registry
- entity_id must exist in the Historical Entity Registry
- no prices
- no benchmarks
- no synthetic labels
- no forecast accuracy claims

## Strategic Role

Forecast engines, dashboards, and future ML pipelines should use this registry as the canonical hardware interface instead of reading vendor-specific registries directly.

## Changelog

### v1

Initial unified hardware registry for selected AMD and Intel accelerator records.
