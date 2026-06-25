# Historical Pricing Registry v1

## Purpose

This registry introduces the schema for historical pricing evidence in AI-RPCT.

It is intentionally empty in v1 because no verified historical pricing observations have been added yet.

## Dataset

Primary dataset: data/historical_pricing_registry.csv

Warehouse copy: warehouse/historical/pricing/historical_pricing_registry.csv

## Governance

Rules:

- no invented prices
- no estimated prices
- no synthetic pricing data
- no benchmark-derived pricing
- no forecast accuracy claims
- every future pricing row must reference relationship_id
- every future pricing row must reference source_id
- every future pricing row must include verification_status

## Allowed Values

price_type:

- on_demand
- reserved
- spot
- marketplace
- contract
- unknown

verification_status:

- verified
- partially_verified
- pending_verification

## Changelog

### v1

Initial pricing evidence schema with zero pricing rows.
