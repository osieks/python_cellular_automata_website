.DEFAULT_GOAL := run

setup: requirements.txt
	pip install -r requirements.txt

run: setup
	python3 app.py