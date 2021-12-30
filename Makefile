setup:
	pip install --user pipenv
	pipenv install

run:
	pipenv run python3 -m artist

test:
	pipenv run python3 -m unittest discover -s tests -p 'test_*.py'

testcase:
	pipenv run python3 -m unittest ${TESTS}

bootstrap:
# Set python path so it can find our artist module.
	PYTHONPATH="." pipenv run python3 scripts/bootstrap.py

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
