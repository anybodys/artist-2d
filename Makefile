setup:
	pip install --user pipenv
	pipenv install

run:
	python3 -m artist

test:
	python3 -m unittest discover -s tests -p 'test_*.py'

testcase:
	python3 -m unittest ${TESTS}

clean:
	find . -name '*~' -delete
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
