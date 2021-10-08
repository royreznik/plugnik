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


JS_LIST=\
	"https://malsup.github.io/jquery.form.js" \
	"http://hayageek.github.io/jQuery-Upload-File/4.0.11/jquery.uploadfile.min.js" \
	"http://code.jquery.com/jquery-1.11.1.min.js"
JS_FOLDER=./server/static/

download: download-js download-test-plugins

download-js:
	for url in $(JS_LIST); do \
		file_name=$$(echo $$url | sed -nr 's#.*/(.*\.js)#\1#p'); \
		file_path=$(JS_FOLDER)$$file_name; \
		test -f $$file_path || wget -O $$file_path $$url; \
	done



PLUGINS_LIST=\
	"https://plugins.jetbrains.com/files/7724/140223/Docker-213.4250.391.zip?updateId=140223&pluginId=7724&family=INTELLIJ" \
	"https://plugins.jetbrains.com/files/9568/140077/go-213.4631.20.zip?updateId=140077&pluginId=9568&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/164/139093/IdeaVim-1.7.2.zip?updateId=139093&pluginId=164&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/10080/134110/intellij-rainbow-brackets-6.21.zip?updateId=134110&pluginId=10080&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/7287/139807/js-karma-213.4631.9.zip?updateId=139807&pluginId=7287&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/9792/130615/Key-Promoter-X-2021.2.zip?updateId=130615&pluginId=9792&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/9333/140246/makefile-213.4250.391.zip?updateId=140246&pluginId=9333&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/14307/135804/poetry-pycharm-plugin.zip?updateId=135804&pluginId=14307&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/631/140102/python-213.4631.20.zip?updateId=140102&pluginId=631&family=INTELLIJ" \
 	"https://plugins.jetbrains.com/files/2162/139458/StringManipulation.zip?updateId=139458&pluginId=2162&family=INTELLIJ"
REAL_PLUGINS_DIR=./tests/resources/real/

download-test-plugins:
	mkdir -p $(REAL_PLUGINS_DIR)
	for url in $(PLUGINS_LIST); do \
		file_name=$$(echo $$url | sed -nr 's#.*\/(.*)\?.*#\1#p'); \
		file_path=$(REAL_PLUGINS_DIR)$$file_name; \
		test -f $$file_path || wget -O $$file_path $$url; \
	done
