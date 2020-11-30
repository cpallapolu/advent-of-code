
clean-pyc:
	find . -name '*.pyc' -exec rm {} +
	find . -name '*.pyo' -exec rm {} +

lint: clean-pyc
	flake8 .

pip-install:
	pip install --no-cache-dir -r ./requirements.txt

run-all-puzzles:
	python src/run.py all
