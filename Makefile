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


download-js:
	[ -f ./server/static/jquery.form.js ] && echo "jquery.form.js already exists, skipping" || wget https://malsup.github.io/jquery.form.js -O server/static/jquery.form.js
	[ -f ./server/static/jquery.uploadfile.min.js ] && echo "jquery.uploadfile.min.js already exists, skipping" || wget http://hayageek.github.io/jQuery-Upload-File/4.0.11/jquery.uploadfile.min.js -O server/static/jquery.uploadfile.min.js
	[ -f ./server/static/jquery-1.11.1.min.js ] && echo "jquery-1.11.1.min.js already exists, skipping" || wget http://code.jquery.com/jquery-1.11.1.min.js -O server/static/jquery-1.11.1.min.js


download-test-plugins:
	mkdir -p ./tests/resources/real/

	[ -f ./tests/resources/real/Docker-213.4250.391.zip ] || wget -O ./tests/resources/real/Docker-213.4250.391.zip https://plugins.jetbrains.com/files/7724/140223/Docker-213.4250.391.zip?updateId=140223&pluginId=7724&family=INTELLIJ
	[ -f ./tests/resources/real/go-213.4631.20.zip ] || wget -O ./tests/resources/real/go-213.4631.20.zip https://plugins.jetbrains.com/files/9568/140077/go-213.4631.20.zip?updateId=140077&pluginId=9568&family=INTELLIJ
	[ -f ./tests/resources/real/IdeaVim-1.7.2.zip ] || wget -O ./tests/resources/real/IdeaVim-1.7.2.zip https://plugins.jetbrains.com/files/164/139093/IdeaVim-1.7.2.zip?updateId=139093&pluginId=164&family=INTELLIJ
	[ -f ./tests/resources/real/intellij-rainbow-brackets-6.21.zip ] || wget -O ./tests/resources/real/intellij-rainbow-brackets-6.21.zip https://plugins.jetbrains.com/files/10080/134110/intellij-rainbow-brackets-6.21.zip?updateId=134110&pluginId=10080&family=INTELLIJ
	[ -f ./tests/resources/real/js-karma-213.4631.9.zip ] || wget -O ./tests/resources/real/js-karma-213.4631.9.zip https://plugins.jetbrains.com/files/7287/139807/js-karma-213.4631.9.zip?updateId=139807&pluginId=7287&family=INTELLIJ
	[ -f ./tests/resources/real/Key-Promoter-X-2021.2.zip ] || wget -O ./tests/resources/real/Key-Promoter-X-2021.2.zip https://plugins.jetbrains.com/files/9792/130615/Key-Promoter-X-2021.2.zip?updateId=130615&pluginId=9792&family=INTELLIJ
	[ -f ./tests/resources/real/makefile-213.4250.391.zip ] || wget -O ./tests/resources/real/makefile-213.4250.391.zip https://plugins.jetbrains.com/files/9333/140246/makefile-213.4250.391.zip?updateId=140246&pluginId=9333&family=INTELLIJ
	[ -f ./tests/resources/real/poetry-pycharm-plugin.zip ] || wget -O ./tests/resources/real/poetry-pycharm-plugin.zip https://plugins.jetbrains.com/files/14307/135804/poetry-pycharm-plugin.zip?updateId=135804&pluginId=14307&family=INTELLIJ
	[ -f ./tests/resources/real/python-213.4631.20.zip ] || wget -O ./tests/resources/real/python-213.4631.20.zip https://plugins.jetbrains.com/files/631/140102/python-213.4631.20.zip?updateId=140102&pluginId=631&family=INTELLIJ
	[ -f ./tests/resources/real/StringManipulation.zip ] || wget -O ./tests/resources/real/StringManipulation.zip https://plugins.jetbrains.com/files/2162/139458/StringManipulation.zip?updateId=139458&pluginId=2162&family=INTELLIJ
