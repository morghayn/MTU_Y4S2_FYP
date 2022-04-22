PROJECT=MTU_Y4S2_DDM_1
PYTHON_VERSION=3.9.7
USER=morgan
PYENV_PATH=/home/${USER}/.pyenv/versions/${PYTHON_VERSION}/bin/python

debug: wsl-host
	${PYENV_PATH} \
	initialization/run.py --debug

# misc.
wsl-host:
	./wsl_host.sh

# initialization application
fresh-install: wsl-host
	${PYENV_PATH} \
	initialization/run.py --create-json --drop-tables --create-tables

lite-update: wsl-host
	${PYENV_PATH} \
	initialization/run.py --create-json --create-tables

insert: wsl-host
	${PYENV_PATH} \
	initialization/run.py --insert

patch: wsl-host
	${PYENV_PATH} \
	initialization/run.py --patch

# containers
update: clean build start
clean:
	docker-compose stop
	docker system prune
build:
	docker-compose build
start:
	docker-compose up

# local app
start-annotator:
	${PYENV_PATH} \
	annotator/app.py