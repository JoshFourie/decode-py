env:
	python3 -m venv env

test:
	pytest --cov-report term:skip-covered --cov-report term-missing --cov src/


test-verbose:
	pytest -s --capture=no --full-trace

setup:
	python3 -m pip install --upgrade pip -r requirements.txt

commit: test
	git add .
	git commit -s

risky-commit:
	git add .
	git commit -s
