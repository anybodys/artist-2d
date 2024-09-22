.PHONY: setup setup-virtual-display run run-api db-migrate db-makemigrations db-shell test clean

setup:
	pip install --upgrade --user pipenv
	pipenv install --dev

setup-virtual-display:
	pipenv run Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

run: run-api

run-api: setup-virtual-display
	pipenv run docker-compose up -d --build

db-migrate:
	pipenv run docker-compose exec api python manage.py migrate --noinput

db-makemigrations:
	pipenv run docker-compose exec api python manage.py makemigrations --noinput

db-shell:
	pipenv run docker-compose exec db psql artist local-user

test: setup-virtual-display
	pipenv run docker-compose -f docker-compose-test.yml up --build --abort-on-container-exit --force-recreate --remove-orphans

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
