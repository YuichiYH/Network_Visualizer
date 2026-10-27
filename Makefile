run:
	python -m flask run

test:
	python -m pytest -v --maxfail=1

freeze:
	pip freeze > requirements.txt