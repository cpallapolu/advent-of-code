
remove-files:
	find ./src -name '*.pyc' -exec rm {} +
	find ./src -name '*.pyo' -exec rm {} +
	find ./src -type d -name __pycache__ -exec rm -rf '{}' +

lint: remove-files
	flake8 .

pip-install: remove-files
	pip install --no-cache-dir -r ./requirements.txt

run-all-puzzles:
	python src/run.py all

generate-markdown:
	python src/docs/generate_readme.py

githooks:
	python -m python_githooks

install: pip-install
	githooks
