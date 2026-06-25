# Historical Entity Registry v1

## Purpose

This registry introduces centralized entity identifiers for AI-RPCT historical datasets.

It prepares the project for source-id migration, entity-id migration, unified hardware registries, and a future AI Infrastructure Knowledge Graph.

## Dataset

Primary dataset: data/historical_entity_registry.csv

Warehouse copy: warehouse/historical/metadata/historical_entity_registry.csv

## Entity Types

Initial coverage:

- vendor
- architecture
- compute_api
- product_family
- gpu

## Governance

Rules:

- every entity has a stable entity_id
- every entity has a source_id
- no prices
- no benchmarks
- no synthetic labels
- no forecast accuracy claims
- ambiguous entities remain excluded until source-backed

## Current Coverage

Initial entities cover:

- AMD
- Intel
- NVIDIA
- CDNA
- CDNA2
- CDNA3
- Ponte Vecchio / Xe-HPC
- Gaudi2
- Gaudi3
- ROCm
- oneAPI
- SynapseAI
- CUDA
- selected AMD and Intel accelerator products

## Changelog

### v1

Initial historical entity registry for vendors, architectures, APIs, product families, and selected GPUs.
