.PHONY: setup run run-api test testcase deploy clean

setup:
	pip install --upgrade --user pipenv
	pipenv install --dev
	npm install -g api-spec-converter

run: run-api

run-api:
	pipenv run flask --app voting.api --debug run

test:
	PIPENV_DOTENV_LOCATION=.env.test pipenv run pytest

testcase:
	PIPENV_DOTENV_LOCATION=.env.test pipenv run pytest ${TESTS}

deploy:
	gcloud run deploy --source . votingapi

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
