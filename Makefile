.PHONY: help install run docker-build docker-up compose-up compose-prod deploy release

help:
	@echo "Available targets:"
	@echo "  install      - install python dependencies"
	@echo "  run          - run the FastAPI app locally"
	@echo "  docker-build - build the docker image"
	@echo "  docker-up    - run the service in docker"
	@echo "  compose-up   - run via docker compose"
	@echo "  compose-prod - run production-style docker compose"

install:
	python3 -m pip install -r requirements.txt

run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t ai-rpct .

docker-up:
	docker run -p 8000:8000 -e AI_RPCT_API_KEYS=${AI_RPCT_API_KEYS:-demo-key} ai-rpct

compose-up:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up --build

compose-prod:
	docker compose -f docker-compose.yml up --build

deploy:
	./deploy.sh

smoke:
	chmod +x scripts/smoke_test.sh || true
	./scripts/smoke_test.sh

release:
	VERSION=$(grep -Eo 'v[0-9]+\.[0-9]+' VERSION.md | head -1)
	if [ -z "$$VERSION" ]; then \
	  echo "Could not read version from VERSION.md"; exit 1; \
	fi
	git tag -a "$$VERSION" -m "Release $$VERSION"
	@echo "Created git tag $$VERSION"
