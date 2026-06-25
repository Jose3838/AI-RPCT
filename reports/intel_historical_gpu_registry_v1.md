# Intel Historical GPU Registry v1

## Purpose

This registry adds a governance-first historical Intel accelerator dataset for AI-RPCT.

The dataset is intended for historical enrichment, explainability, and future feature-store use.

It intentionally excludes:

- synthetic benchmarks
- invented historical prices
- forecast accuracy claims
- synthetic labels

## Dataset

Primary dataset

```
data/intel_historical_gpu_registry.csv
```

Warehouse copy

```
warehouse/historical/intel/intel_historical_gpu_registry.csv
```

## Scope

Current coverage

- Intel Data Center GPU Max 1100
- Intel Gaudi2
- Intel Gaudi 3 announcement reference
- Intel Gaudi 3 launch reference

## Governance

Rules:

- source-backed records only
- missing information remains empty
- quarter-level launch dates remain quarter-level
- no inferred day-level dates
- no generated prices
- no benchmark claims

## Known Gaps

Future versions may include:

- Intel Data Center GPU Max 1550
- Intel Data Center GPU Max 1350
- Intel Gaudi first generation
- Intel Greco
- China-specific Gaudi variants only if source-backed and clearly separated

## Changelog

### v1

Initial Intel historical accelerator registry.
