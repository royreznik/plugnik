run: build
	docker-compose up

build:
	docker-compose build

lint:
	poetry run flake8 server
	poetry run mypy server

format:
	poetry run black server
	poetry run isort server