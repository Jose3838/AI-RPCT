# AMD Historical GPU Registry v1

## Purpose

This registry adds a governance-first historical AMD GPU dataset for AI-RPCT.

The dataset is intended for historical enrichment, explainability, and future feature-store use.

It intentionally excludes:

- synthetic benchmarks
- invented historical prices
- forecast accuracy claims
- synthetic labels

## Dataset

Primary dataset

```
data/amd_historical_gpu_registry.csv
```

Warehouse copy

```
warehouse/historical/amd/amd_historical_gpu_registry.csv
```

## Scope

Current coverage

- AMD Instinct MI100
- AMD Instinct MI200 Series
- AMD Instinct MI210
- AMD Instinct MI300X

## Governance

This registry follows AI-RPCT governance principles.

Rules:

- historical facts only
- source-backed records only
- missing information remains empty
- no inferred values
- no generated prices
- no benchmark claims

## Known Gaps

Future versions may include

- MI250
- MI250X
- MI300A
- MI325X

only after source verification.

## Changelog

### v1

Initial AMD historical registry.
