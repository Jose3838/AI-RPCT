# Historical Capacity Registry v1

## Purpose

This registry introduces historical capacity observations for AI-RPCT.

It links capacity observations to provider relationships instead of directly duplicating provider, hardware, or software fields.

## Dataset

Primary dataset: data/historical_capacity_registry.csv

Warehouse copy: warehouse/historical/capacity/historical_capacity_registry.csv

## Scope

Initial coverage includes selected provider relationship capacity observations.

This registry does not claim complete market coverage.

## Governance

Rules:

- relationship_id must exist in Provider Relationship Registry
- source_id must exist in Historical Source Registry
- no pricing data
- no forecast accuracy claims
- no synthetic labels
- no inferred market-wide capacity
- observations are point-in-time records

## Allowed Values

capacity_status:

- available
- limited
- unavailable

availability_level:

- high
- medium
- low
- unknown

## Changelog

### v1

Initial historical capacity registry with selected point-in-time observations.
