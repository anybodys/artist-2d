.PHONY: setup run run-api test testcase deploy clean

setup:
	pip install --upgrade --user pipenv
	pipenv install --dev
	npm install -g api-spec-converter

run: run-api

run-api:
	pipenv run docker-compose up -d --build

db-migrate:
	pipenv run docker-compose exec api python manage.py migrate --noinput

db-makemigrations:
	pipenv run docker-compose exec api python manage.py makemigrations --noinput

db-shell:
	pipenv run docker-compose exec db psql artist local-user

test:
	pipenv run docker-compose -f docker-compose-test.yml up --build --abort-on-container-exit

deploy:
	gcloud run deploy --source . storageapi

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
