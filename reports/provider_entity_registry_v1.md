# Provider Entity Registry v1

## Purpose

This registry introduces provider entities for AI-RPCT.

It links cloud provider records to stable entity identifiers so future capacity, pricing, relationship, and feature-store datasets can reference providers consistently.

## Dataset

Primary dataset: data/provider_entity_registry.csv

Warehouse copy: warehouse/historical/providers/provider_entity_registry.csv

## Scope

Initial coverage:

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

- every provider entity has a stable entity_id
- every provider entity links to provider_id
- provider_id must exist in Cloud Provider Registry v2
- source_id must exist in Historical Source Registry
- no pricing data
- no capacity claims
- no availability claims
- no forecast accuracy claims

## Changelog

### v1

Initial provider entity registry.
