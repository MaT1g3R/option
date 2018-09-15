.PHONY: docs test publish

test:
	pytest

docs:
	PYTHONPATH=.. make -C docs html

publish:
	poetry build
	poetry publish
