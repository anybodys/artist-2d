.PHONY: setup run run-api test testcase deploy clean

setup:
	pip install --upgrade --user pipenv
	pipenv install --dev
	npm install -g api-spec-converter

run: run-api

run-api:
	pipenv run python manage.py runserver

test:
	PIPENV_DOTENV_LOCATION=.env.test pipenv run python manage.py test

deploy:
	gcloud run deploy --source . storageapi

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
