# Provider Relationship Registry v1

## Purpose

This registry introduces provider-to-technology relationships for AI-RPCT.

It models supported APIs and offered accelerator hardware as explicit graph relationships.

## Dataset

Primary dataset:

data/provider_relationship_registry.csv

Warehouse copy:

warehouse/historical/providers/provider_relationship_registry.csv

## Scope

Relationship types:

- supports
- offers

Current providers:

- AWS
- Azure
- Google Cloud
- CoreWeave
- Lambda

## Governance

Rules

- relationship_id must be unique
- provider_entity_id must exist
- target_entity_id must exist
- source_id must exist
- no inferred relationships
- no synthetic relationships

## Changelog

### v1

Initial provider relationship registry.
