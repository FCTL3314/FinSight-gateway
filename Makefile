# Application
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Docker services
LOCAL_DOCKER_COMPOSE_PROJECT_NAME=auth_services_local
LOCAL_DOCKER_COMPOSE_FILE_PATH=./docker/local/docker-compose.yml

up_local_services:
	docker compose -p $(LOCAL_DOCKER_COMPOSE_PROJECT_NAME) -f $(LOCAL_DOCKER_COMPOSE_FILE_PATH) up -d

down_local_services:
	docker compose -p $(LOCAL_DOCKER_COMPOSE_PROJECT_NAME) -f $(LOCAL_DOCKER_COMPOSE_FILE_PATH) down

restart_local_services: down_local_services up_local_services

local_services_logs:
	docker compose -p $(LOCAL_DOCKER_COMPOSE_PROJECT_NAME) -f $(LOCAL_DOCKER_COMPOSE_FILE_PATH) logs

# Migrations(Goose)
MIGRATIONS_DIR=migrations
POSTGRES_DSN_DEFAULT=postgresql://postgres:postgres@127.0.0.1:5432/postgres?sslmode=disable

apply_migrations:
	goose -dir $(MIGRATIONS_DIR)  postgres "$(or $(POSTGRES_DSN), $(POSTGRES_DSN_DEFAULT))" up

add_migration:
	goose -dir $(MIGRATIONS_DIR) create $(name) sql

# Deployment
build_prod_image:
	docker build -f .\docker\prod\Dockerfile .
