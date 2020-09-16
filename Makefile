install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=mylib --cov=spotiplay test_spotiplay.py


lint:
	pylint --disable=R,C spotiplay.py test_spotiplay.py

format:
	black *.py

all: install lint test
