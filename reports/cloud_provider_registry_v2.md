# Cloud Provider Registry v2

## Purpose

This registry expands AI-RPCT cloud provider coverage beyond hyperscalers.

It introduces GPU cloud and GPU marketplace providers for future capacity, pricing, and availability registries.

## Dataset

Primary dataset: data/cloud_provider_registry_v2.csv

Warehouse copy: warehouse/historical/providers/cloud_provider_registry_v2.csv

## Scope

Initial provider coverage:

- Amazon Web Services
- Microsoft Azure
- Google Cloud
- CoreWeave
- Lambda
- Crusoe
- Nebius
- RunPod
- Vast.ai

## Governance

Rules:

- source_id must exist in Historical Source Registry
- no pricing data
- no capacity claims
- no availability claims
- no forecast accuracy claims
- unverified fields remain empty

## Changelog

### v2

Expanded cloud provider registry with GPU cloud and GPU marketplace providers.
