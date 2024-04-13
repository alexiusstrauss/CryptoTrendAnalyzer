SHELL := /bin/bash
FILES=$(shell docker ps -a -q --filter "name=cryptotrendanalyzer*")

# Verifica versao do docker compose.
COMPOSE_COMMAND=$(shell command -v docker-compose >/dev/null 2>&1 && echo "docker-compose" || echo "docker compose")

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf app/src/db.sqlite3
	rm -rf app/.pytest_cache

create-requirements:
	pipenv requirements > contrib/requirements.txt

setup:
	@if [ ! -f app/.env ]; then \
		cp ./contrib/.env-exemple app/.env; \
		echo "Arquivo .env criado na pasta app/"; \
	fi

build:
	docker build -t cryptotrendanalyzer-api:latest .

up: build
	$(COMPOSE_COMMAND) up -d

up-log: up
	docker logs -f cryptotrendanalyzer-api

crontab-add:
	docker exec -it cryptotrendanalyzer-api pipenv run python manage.py crontab add

crontab-show:
	docker exec -it cryptotrendanalyzer-api pipenv run python manage.py crontab show

check-missing-days:
	docker exec -it cryptotrendanalyzer-api pipenv run python manage.py check_missing_days

verify-makrket-data:
	docker exec -it cryptotrendanalyzer-api pipenv run python manage.py verify_and_load_data

down:
	$(COMPOSE_COMMAND) down

up-localy:
	python app/manage.py runserver

bash:
	docker exec -ti cryptotrendanalyzer-api bash

logs-api:
	docker logs -f cryptotrendanalyzer-api

test:
	docker exec -it cryptotrendanalyzer-api pipenv run pytest

test-coverage:
	docker exec -it cryptotrendanalyzer-api pipenv run pytest --cov=.

test-cov-report:
	docker exec -it cryptotrendanalyzer-api pipenv run pytest -vvv --cov-report html --cov=.

isort:
	@isort -m 3 --trailing-comma --use-parentheses --honor-noqa  app/. --verbose --diff

style:
	@isort -m 3 --trailing-comma --use-parentheses --honor-noqa  app/.
	@black -S -t py37 -l 120 app/. --exclude '/(\.git|\.venv|env|venv|build|dist)/'

lint:
	pylint app/

pre-commit:
	@echo "Executando verificação de estilo e testes de cobertura..."
	@{ \
		make style && \
		make test-coverage; \
	} || { \
		echo "Erro ao validar o código ou testes"; \
		exit 1; \
	}
	@echo "Validação efetuada com sucesso"

.PHONY: all clean install test
