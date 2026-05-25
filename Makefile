.PHONY: setup test build run stop clean lint deploy

PYTHON := python3
NODE := node
GO := go
DOCKER := docker
DOCKER_COMPOSE := docker-compose

setup:
	./src/scripts/setup.sh

test:
	cd src/engine && $(PYTHON) -m pytest tests/ -v --tb=short
	cd src/scanner && $(GO) test -v ./...
	cd src/web && npx vitest run

test-python:
	cd src/engine && $(PYTHON) -m pytest tests/engine/ -v --tb=short

test-go:
	cd src/scanner && $(GO) test -v ./...

test-web:
	cd src/web && npx vitest run

lint:
	cd src/engine && ruff check . && mypy .
	cd src/scanner && golangci-lint run
	cd src/web && npx eslint . --ext .ts,.tsx

build:
	cd src/web && npm run build
	cd src/scanner && $(GO) build -o bin/scanner main.go

run:
	$(DOCKER_COMPOSE) up -d

stop:
	$(DOCKER_COMPOSE) down

clean:
	$(DOCKER_COMPOSE) down -v
	rm -rf bin/ src/web/.next/ src/web/node_modules/

deploy:
	./src/scripts/deploy.sh

db-init:
	psql $(DATABASE_URL) -f src/db/schema.sql
	psql $(DATABASE_URL) -f src/db/seed.sql

db-migrate:
	for f in src/db/migrations/*.sql; do psql $(DATABASE_URL) -f $$f; done

monitor:
	./src/scripts/monitor.sh

health:
	./src/scripts/health-check.sh

backup:
	./src/scripts/backup.sh
