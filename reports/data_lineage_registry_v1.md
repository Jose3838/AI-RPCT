# Data Lineage Registry v1

## Purpose

This registry documents dataset lineage for AI-RPCT.

It records which builders generate which output datasets and which input datasets they depend on.

## Dataset

Primary dataset: data/data_lineage_registry.csv

Warehouse copy: warehouse/metadata/data_lineage_registry.csv

## Governance

Rules:

- lineage records document pipeline dependencies
- no synthetic labels
- no pricing claims
- no accuracy claims
- no ML promotion claims

## Changelog

### v1

Initial data lineage registry for feature store, forecast dataset, forecast engine output, and forecast explanations.
