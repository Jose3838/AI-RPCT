# Historical Source Registry v1

## Purpose

This registry introduces a centralized source catalog for AI-RPCT historical datasets.

The goal is to make historical data governance more consistent, auditable, and reusable across registries.

## Dataset

Primary dataset

```
data/historical_source_registry.csv
```

Warehouse copy

```
warehouse/historical/metadata/historical_source_registry.csv
```

## Scope

Initial official source coverage:

- AMD Investor Relations
- AMD Product Pages
- Intel Newsroom
- Intel Product Specifications
- NVIDIA Newsroom
- NVIDIA Product Pages
- NVIDIA CUDA Documentation
- AMD ROCm Documentation

## Governance

Rules:

- only source metadata is stored
- no prices
- no benchmarks
- no forecast accuracy claims
- no synthetic labels
- every source has a stable source_id
- verification_level is explicit

## Migration Strategy

Existing historical registries may keep source_url temporarily.

Future versions should add source_id while preserving backward compatibility.

A later migration can move registries from direct source_url references to source_id-based references.

## Changelog

### v1

Initial centralized historical source registry.
