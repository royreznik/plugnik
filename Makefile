run: build
	docker-compose -f docker-compose.prod.yml up

build:
	docker-compose -f docker-compose.prod.yml build

run-dev: build-dev
	docker-compose -f docker-compose.dev.yml up

build-dev:
	docker-compose -f docker-compose.dev.yml build

lint:
	poetry run flake8 server
	poetry run mypy server

format:
	poetry run black --target-version py39 server
	poetry run isort --py 39 server
