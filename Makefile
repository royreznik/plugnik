run: build
	docker-compose up

run-dev: build
	docker-compose -f docker-compose.dev.yml up

build:
	docker-compose build

lint:
	poetry run flake8 server
	poetry run mypy server

format:
	poetry run black --target-version py39 server
	poetry run isort --py 39 server
