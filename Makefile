.PHONY: docs test publish lint

test:
	python -m pytest -vvv -s tests

docs:
	PYTHONPATH=.. make -C docs html
	touch docs/_build/html/.nojekyll

lint:
	mypy option
	pylint option
