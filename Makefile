
clean-files:
	find . -name '*.pyc' -exec rm {} +
	find . -name '*.pyo' -exec rm {} +

lint: clean-files
	flake8 .

pip-install:
	pip install --no-cache-dir -r ./requirements.txt

run-all-puzzles:
	python src/run.py all

githooks:
	python -m python_githooks
