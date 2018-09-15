.PHONY: docs test publish lint

test:
	python -m pytest -vvv -s tests

cov:
	python -m pytest -vvv -s --cov=ene tests
	pip install codecov
	codecov

docs:
	PYTHONPATH=.. make -C docs html
	cp -r docs/_build/html/* docs/

publish:
	poetry build
	poetry publish

lint:
	mypy option
	pylint option

ci_install:
	pip install poetry
	poetry install
