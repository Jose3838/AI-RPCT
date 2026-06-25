# Unified Software Stack Registry v1

## Purpose

This registry introduces a canonical software-stack layer for AI-RPCT.

It provides a unified view across vendor-specific historical software timelines such as CUDA, ROCm, oneAPI, and SynapseAI.

## Dataset

Primary dataset: data/unified_software_stack_registry.csv

Warehouse copy: warehouse/historical/metadata/unified_software_stack_registry.csv

## Scope

Initial coverage:

- CUDA
- ROCm
- oneAPI
- SynapseAI

## Governance

Rules:

- every software record has a stable software_id
- every software record links to a source_id
- source_id must exist in the Historical Source Registry
- no prices
- no benchmarks
- no synthetic labels
- no forecast accuracy claims

## Strategic Role

Forecast engines, dashboards, and future ML pipelines should use this registry as the canonical software-stack interface instead of reading vendor-specific timelines directly.

## Changelog

### v1

Initial unified software stack registry for selected CUDA, ROCm, oneAPI, and SynapseAI records.
