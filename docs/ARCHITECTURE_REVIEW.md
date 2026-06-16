# AI-RPCT Architecture Review

## Current Architecture

- collectors: gather market and GPU data
- analytics: derive rankings, forecasts, alerts and reports
- api: expose data via FastAPI
- dashboard: generate local HTML dashboard
- database: SQLite persistence
- security: API keys and usage tracking
- docs: product and deployment documentation

## Next Technical Priority

The system should now focus on real GPU provider data instead of adding more placeholder analytics.

## Recommended Next Steps

1. Implement one real provider API.
2. Add API tests.
3. Move secrets to environment variables.
4. Deploy to a small VPS.
5. Collect real data for 30 days.
