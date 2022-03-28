PROJECT=MTU_Y4S2_DDM_1
PYTHON_VERSION=3.9.7
USER=morgan
PYENV_PATH=/home/${USER}/.pyenv/versions/${PYTHON_VERSION}/bin/python

init:
	${PYENV_PATH} \
	initialization/run.py --create-json --init --del