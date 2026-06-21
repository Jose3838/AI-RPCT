# AI-RPCT Deployment

## Local API

./start_api.sh

Open:

http://127.0.0.1:8000/docs

## Docker Build

docker build -t ai-rpct .

## Docker Run

docker run -p 8000:8000 -e AI_RPCT_API_KEYS=demo-key ai-rpct

A `.dockerignore` file is included to reduce build context size and avoid copying local artifacts.

## Production Docker Build

docker build -f Dockerfile.prod -t ai-rpct:prod .

docker run -p 8000:8000 -e AI_RPCT_API_KEYS=prod-key ai-rpct:prod

## Docker Compose

Production-style deploy:

docker compose -f docker-compose.yml up --build

Local development with live source and data mounting:

docker compose -f docker-compose.yml -f docker-compose.override.yml up --build

The container healthcheck is wired to `GET /health`.

## Makefile

Use the Makefile for common workflows:

make install
make run
make compose-up
make compose-prod
make release

## Deployment script

For a one-step production launch, set API keys and run:

```bash
export AI_RPCT_API_KEYS="prod-key-1,prod-key-2"
./deploy.sh
```

## Production Notes

Recommended first deployment:

- Hetzner VPS
- Docker
- FastAPI
- SQLite for MVP
- Daily cron pipeline
- Later migration to PostgreSQL/TimescaleDB
