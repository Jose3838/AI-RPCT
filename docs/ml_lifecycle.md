# ML Lifecycle

AI-RPCT separates forecasts from true future outcomes.

## Lifecycle

1. Generate forecast
2. Store forecast snapshot
3. Create forecast outcome windows
4. Wait for windows to mature
5. Resolve true future outcome labels
6. Build Training Dataset v3
7. Allow retraining only when enough true labels exist
8. Benchmark challenger models
9. Promote only if governance gates pass

## Current State

- True outcome labels prepared: yes
- Trainable true labels: 0
- Training Dataset v3: not_ready
- Auto retraining: waiting_for_labels

This prevents fake accuracy caused by current-state labels or target leakage.
