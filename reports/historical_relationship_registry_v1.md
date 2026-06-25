# Historical Relationship Registry v1

## Purpose

This registry introduces explicit relationships between historical AI infrastructure entities.

It is the first CSV-based foundation for the future AI-RPCT Knowledge Graph.

## Dataset

Primary dataset: data/historical_relationship_registry.csv

Warehouse copy: warehouse/historical/metadata/historical_relationship_registry.csv

## Relationship Types

Initial coverage:

- uses_architecture
- uses_compute_api
- member_of_family

## Governance

Rules:

- every relationship has a stable relationship_id
- every source_entity_id must exist in the Historical Entity Registry
- every target_entity_id must exist in the Historical Entity Registry
- every source_id must exist in the Historical Source Registry
- no prices
- no benchmarks
- no synthetic labels
- no forecast accuracy claims

## Changelog

### v1

Initial relationship registry connecting selected GPUs, architectures, compute APIs, and product families.
