#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ -z "${AI_RPCT_API_KEYS:-}" ]; then
  echo "ERROR: AI_RPCT_API_KEYS is not set."
  echo "Set API keys before deploying, e.g. export AI_RPCT_API_KEYS=prod-key"
  exit 1
fi

IMAGE_NAME="ai-rpct:prod"
CONTAINER_NAME="ai-rpct-prod"

echo "Building production image..."
docker build --pull -f Dockerfile.prod -t "${IMAGE_NAME}" .

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Found existing container ${CONTAINER_NAME}, stopping and removing it..."
  docker rm -f "${CONTAINER_NAME}"
fi

echo "Running production container..."
docker run -d --restart unless-stopped --name "${CONTAINER_NAME}" -p 8000:8000 \
  -e AI_RPCT_API_KEYS="${AI_RPCT_API_KEYS}" \
  "${IMAGE_NAME}"

echo "Deployment complete."
echo "Access the service at http://127.0.0.1:8000/web"
