# AI-RPCT Release Notes

Current Version: v66.0
Release Date: 2026-06-21

## Summary

AI-RPCT v66.0 is a production-ready public beta terminal release focused on secure PDF reports, deployment automation, and healthcheck-managed container delivery.

## Highlights

- Secure PDF export/download endpoints with `X-API-KEY` auth
- ReportLab-powered branded customer report PDF
- Docker production image via `Dockerfile.prod`
- Compose deployment with `docker-compose.yml` and local override
- Health endpoints: `/health` and `/ready`
- Release automation via `deploy.sh`
- Enhanced README and deployment documentation
- Makefile targets for local and container workflows

## Notes

- API keys are configured via `AI_RPCT_API_KEYS`
- Docker compose healthcheck uses `GET /health`
- Local development uses `docker-compose.override.yml`
- Production image builds from `Dockerfile.prod`

## Next steps

- Add multi-tenant auth and organization-level API access
- Complete KPI endpoint coverage for dashboards
- Harden production-grade user/accounts and billing flows
- Validate provider data feeds and forecast accuracy
