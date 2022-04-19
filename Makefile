PROJECT=MTU_Y4S2_DDM_1
PYTHON_VERSION=3.9.7
USER=morgan
PYENV_PATH=/home/${USER}/.pyenv/versions/${PYTHON_VERSION}/bin/python

debug: wsl-host
	${PYENV_PATH} \
	initialization/run.py --debug

wsl-host:
	./wsl_host.sh

install: wsl-host
	${PYENV_PATH} \
	initialization/run.py --drop-tables --create-json --init-insert

update: clean build start
clean:
	docker-compose stop
	docker system prune
build:
	docker-compose build
start:
	docker-compose up