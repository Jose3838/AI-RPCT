# Real Provider Integration

Goal:

Replace placeholder GPU data with real provider API data.

Priority providers:

1. RunPod
2. Vast.ai
3. Lambda Labs
4. CoreWeave
5. Akash

Required fields:

- provider
- gpu
- price_per_hour
- availability
- region
- timestamp

Implementation rule:

Every provider connector must return a list of dictionaries with the same schema.
