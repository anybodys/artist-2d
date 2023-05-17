setup:
	pip install --user pipenv
	pipenv install

setup-virtual-display:
	pipenv run Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

run-api:
	pipenv run python3 -m painter.api

run-script:
	pipenv run python3 -m painter

test:
	pipenv run python3 -m unittest discover -s tests -p 'test_*.py'

testcase:
	pipenv run python3 -m unittest ${TESTS}

deploy:
	gcloud run deploy --source . painter-api


bootstrap:
# Set python path so it can find our painter module.
	PYTHONPATH="." pipenv run python3 scripts/bootstrap.py

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
