JS_DIR = ./taiwan/coffee

DATE=$(shell date +%I:%M%p)
CHECK=\033[32m✔\033[39m
DONE="\n${CHECK} Done.\n"
HR=\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#

#
# build and run server
#
build: js
	@echo "\n\nRunning easter..."
	@./manage.py runserver 0.0.0.0:8000

#
# BUILD JS
#
js:
	@echo "\n\n`date` Building JS..."
	@cd ${JS_DIR};	make -s
	@echo ${DONE}

pull:
	@echo "\n\nPulling code from upstream..."
	@git pull --rebase

pip:
	@echo "\n\nInstall dependencies..."
	@pip install -r requirements.txt
	@echo ${DONE}

#
# schema migration and collect static
#
collect:
	@echo "\n\nCollecting static files..."
	@./manage.py collectstatic
	@echo ${DONE}

#
# WATCH JS FILES
#

watch:
	@echo "Watching js files..."; \
	watchr -e "watch('taiwan/coffee/.*\.coffee') { system 'make js' }"



.PHONY: collect watch js pip pull
