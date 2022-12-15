
remove-files:
	find ./src -name '*.pyc' -exec rm {} +
	find ./src -name '*.pyo' -exec rm {} +
	find ./src -type d -name __pycache__ -exec rm -rf '{}' +

lint: remove-files
	flake8 . --count

pip-install: remove-files
	pip install --no-cache-dir -r ./requirements.txt

run:
	nodemon --exec 'echo "\x1B[2J\x1B[3J\x1B[H" && python3' src/run.py

run-all-puzzles:
	python src/run.py --all_puzzles

run-year-puzzles:
	python src/run.py --all_puzzles --year $(year)

run-cache-puzzles:
	python src/run.py --cache

generate-markdown:
	python docs/generate_readme.py

githooks:
	python -m python_githooks

install: pip-install
	githooks
