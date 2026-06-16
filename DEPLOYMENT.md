# AI-RPCT Deployment

## Local API

./start_api.sh

Open:

http://127.0.0.1:8000/docs

## Docker Build

docker build -t ai-rpct .

## Docker Run

docker run -p 8000:8000 ai-rpct

## Production Notes

Recommended first deployment:

- Hetzner VPS
- Docker
- FastAPI
- SQLite for MVP
- Daily cron pipeline
- Later migration to PostgreSQL/TimescaleDB
