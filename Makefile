.PHONY: docs test publish lint

test:
	python -m pytest -vvv -s tests

cov:
	python -m pytest -vvv -s --cov=option tests
	pip install codecov
	codecov

docs:
	PYTHONPATH=.. make -C docs html
	touch docs/_build/html/.nojekyll

lint:
	mypy option
	pylint option
