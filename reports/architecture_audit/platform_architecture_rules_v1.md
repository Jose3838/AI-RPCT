# AI-RPCT Platform Architecture Rules v1

## Mission

AI-RPCT is a Decision Intelligence Platform for AI infrastructure.

Every technical decision must support one of these goals:

- improve decision quality
- increase trust
- strengthen the data moat
- improve forecast and recommendation quality
- make the platform easier to operate and scale

---

## Core Principle

AI-RPCT does not build isolated scripts.

AI-RPCT builds platform assets.

---

## Platform Layers

### 1. Collection

Purpose:

Collect raw provider, GPU, cloud, pricing, capacity, and market information.

Examples:

- collectors/
- providers/connectors/
- warehouse/raw_providers/
- warehouse/live_provider_history/
- warehouse/snapshots/

Rule:

Collectors must write raw or snapshot data. They must not contain decision logic.

---

### 2. Registry

Purpose:

Normalize entities, providers, accelerators, relationships, and metadata.

Examples:

- provider registries
- accelerator registries
- historical registries
- metadata registries

Rule:

Registries are governed sources of truth. They must be reproducible.

---

### 3. Intelligence

Purpose:

Transform normalized data into signals.

Examples:

- scarcity signals
- provider rankings
- market signals
- trend signals
- risk signals

Rule:

Signals must be explainable and traceable to input assets.

---

### 4. Forecast

Purpose:

Predict future conditions.

Examples:

- feature store
- forecast dataset
- forecast output
- forecast explanations
- forecast run summary

Rule:

No production forecast claim is allowed without outcome validation.

---

### 5. Decision

Purpose:

Turn intelligence and forecasts into recommendations.

Examples:

- decision summary
- decision history
- procurement recommendations
- provider recommendations
- capacity recommendations

Rule:

Every recommendation must include confidence, rationale, and evidence.

---

### 6. Governance

Purpose:

Track quality, lineage, metadata, validation, and release state.

Examples:

- asset registry
- asset lineage registry
- module registry
- data quality metrics
- pipeline health
- registry metadata

Rule:

Every important asset must be discoverable and traceable.

---

### 7. Platform

Purpose:

Expose and operate the system.

Examples:

- FastAPI
- Web Console
- DuckDB
- reports
- tests
- CI/CD

Rule:

Platform surfaces must reuse existing assets and avoid duplicate business logic.

---

## Pipeline Rules

There must be one official pipeline entry point:

```bash
python analytics/run_pipeline.py
