# Unified Accelerator Registry v1

## Purpose

This registry introduces a canonical accelerator layer for AI-RPCT.

It sits above the Unified Hardware Registry and normalizes hardware records into accelerator-oriented categories for future feature-store, explainability, and forecast development.

## Dataset

Primary dataset: data/unified_accelerator_registry.csv

Warehouse copy: warehouse/historical/metadata/unified_accelerator_registry.csv

## Scope

Initial coverage includes selected AMD, Intel, and NVIDIA accelerator records.

Vendors:

- AMD
- Intel
- NVIDIA

Accelerator types:

- GPU
- AI Accelerator

## Governance

Rules:

- every accelerator record has a stable accelerator_id
- every accelerator links to a hardware_id
- every accelerator links to an entity_id
- every accelerator links to a source_id
- hardware_id must exist in the Unified Hardware Registry
- entity_id must exist in the Historical Entity Registry
- source_id must exist in the Historical Source Registry
- no prices
- no benchmarks
- no synthetic labels
- no forecast accuracy claims

## Strategic Role

This registry creates a vendor-neutral accelerator interface for future derived features.

Future models should reason over accelerator classes, architectures, compute APIs, and generations instead of raw product names alone.

## Changelog

### v1

Initial unified accelerator registry for selected AMD, Intel, and NVIDIA accelerator records.
