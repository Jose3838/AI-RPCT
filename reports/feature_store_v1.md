# Feature Store v1

## Purpose

The Feature Store provides machine-learning ready features derived from governed AI-RPCT registries.

It is the bridge between registry data and downstream forecasting models.

## Dataset

Primary dataset:

data/feature_store.csv

Warehouse copy:

warehouse/feature_store/feature_store.csv

## Current Features

- provider_id
- entity_id
- vendor
- hardware_type
- architecture
- software_stack
- capacity_status
- availability_level

## Governance

Rules

- features originate from governed registries
- no synthetic provider identities
- no invented hardware
- no inferred pricing
- no forecast labels

## Changelog

### v1

Initial ML feature store.
