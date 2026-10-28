run:
	docker run --rm -p 5000:5000 network_visualizer

test:
	python -m pytest -v

freeze:
	pip freeze > requirements.txt

build:
	docker build -t network_visualizer .

stop:
	docker stop network_visualizer