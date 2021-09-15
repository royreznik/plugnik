run: build
	docker run -p 80:80 --rm jetbrains-server

build:
	docker build -f Dockerfile . --tag jetbrains-server


lint:
	poetry run flake8 server
	poetry run mypy server

format:
	poetry run black server
	poetry run isort server