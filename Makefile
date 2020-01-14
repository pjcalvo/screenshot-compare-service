TESTS_FOLDER?=tests
APP_FOLDER?=vvs

PYTHON_PATH?=../
FLASK_APP?=${APP_FOLDER}/run.py
GUNICRORN_APP?=${APP_FOLDER}.run:app


serve-flask:
	echo "Build and serve app using FLASK dev server"
	FLASK_APP=${FLASK_APP} GOOGLE_APPLICATION_CREDENTIALS=google.json FLASK run

serve:
	GOOGLE_APPLICATION_CREDENTIALS=google.json
	echo "Build and serve app using FLASK dev server"
	gunicorn ${GUNICRORN_APP}
	
test-unit:
	echo "Run Unit Tests"
	PYTHONPATH=${PYTHON_PATH} ENV_FOR_DYNACONF=testing coverage run -m pytest ${TESTS_FOLDER}/*

coverage:
	echo "Run Unit Tests and Codecoverage"
	PYTHONPATH=${PYTHON_PATH} ENV_FOR_DYNACONF=testing coverage run -m pytest ${TESTS_FOLDER}/*
	coverage report

codestyle:
	echo "Code Style Check - Code"
	pycodestyle ${APP_FOLDER}/* --config=.pycodestyle
	echo "Code Style Check - Tests"
	pycodestyle ${TESTS_FOLDER}/* --config=.pycodestyle
