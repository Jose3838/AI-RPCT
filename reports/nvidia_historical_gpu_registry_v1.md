# NVIDIA Historical GPU Registry v1

## Purpose

This registry introduces a historical NVIDIA GPU registry for AI-RPCT.

It provides source-backed NVIDIA accelerator records for historical enrichment, explainability, and future feature-store development.

## Dataset

Primary dataset:

data/nvidia_historical_gpu_registry.csv

Warehouse copy:

warehouse/historical/nvidia/nvidia_historical_gpu_registry.csv

## Scope

Initial coverage:

- Tesla K80
- Tesla V100
- A100
- H100
- B200

## Governance

Rules:

- source-backed historical records only
- no invented launch dates
- no benchmark claims
- no inferred pricing
- no synthetic labels
- future versions may add verification_status

## Known Gaps

Future versions may include:

- P100
- P40
- T4
- L4
- L40
- H200
- GB200

only after source verification.

## Changelog

### v1

Initial NVIDIA historical GPU registry.
