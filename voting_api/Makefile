.PHONY: setup run run-api test testcase deploy clean

setup:
	pip install --upgrade --user pipenv
	pipenv install --dev

generate-openapi:
	pipenv run flask --app voting.api spec 

run: run-api

run-api:
	pipenv run flask --app voting.api --debug run

test:
	PIPENV_DOTENV_LOCATION=.env.test pipenv run pytest

testcase:
	PIPENV_DOTENV_LOCATION=.env.test pipenv run pytest ${TESTS}

deploy:
	gcloud run deploy --source . voting_api

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
