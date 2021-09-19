run: build
	docker-compose -f docker-compose.prod.yml up

build:
	docker build -f Dockerfile . -t plugnik

run-dev: build-dev
	docker-compose -f docker-compose.dev.yml up

build-dev:
	docker-compose -f docker-compose.dev.yml build

lint:
	poetry run flake8 server tests
	poetry run mypy server tests

format:
	poetry run black --target-version py39 server tests
	poetry run isort --py 39 server tests

test:
	cd tests && poetry run pytest . && cd ..

install:
	[ -f ./server/static/jquery.form.js ] && echo "jquery.form.js already exists, skipping" || wget https://malsup.github.io/jquery.form.js -O server/static/jquery.form.js
	[ -f ./server/static/jquery.uploadfile.min.js ] && echo "jquery.uploadfile.min.js already exists, skipping" || wget http://hayageek.github.io/jQuery-Upload-File/4.0.11/jquery.uploadfile.min.js -O server/static/jquery.uploadfile.min.js
	[ -f ./server/static/jquery-1.11.1.min.js ] && echo "jquery-1.11.1.min.js already exists, skipping" || wget http://code.jquery.com/jquery-1.11.1.min.js -O server/static/jquery-1.11.1.min.js
