.PHONY: docs test publish lint

test:
	python -m pytest -vvv -s tests

cov:
	python -m pytest -vvv -s --cov=option tests
	pip install codecov
	codecov

docs:
	PYTHONPATH=.. make -C docs html

publish:
	poetry build
	poetry publish

lint:
	mypy option
	pylint option

ci_install:
	pip install poetry
	poetry install
