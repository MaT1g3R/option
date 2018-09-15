.PHONY: docs test publish

test:
	pytest

docs:
	PYTHONPATH=.. make -C docs html
	cp -r docs/_build/html/* docs/

publish:
	poetry build
	poetry publish

lint:
	mypy option
	pylint option
