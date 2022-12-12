from datetime import datetime
from os.path import abspath, dirname, join

from markdown import markdown
from markdown_include.include import MarkdownInclude

markdown_include = MarkdownInclude(
    configs={
        'inheritHeadingDepth': True,
        'base_path': './docs/',
    },
)
curr_year = datetime.now().year
docs_path = dirname(abspath(__file__))
root_path = abspath(join(docs_path, '../'))
year_path = abspath(join(docs_path, f'../src/years/{curr_year}/'))


def previous_years():
    arr = ['### Years']

    for year in range(2020, curr_year + 1):
        complete_path = f'./src/years/{year}'

        badges = [
            '<img alt="" src="https://img.shields.io/badge/day%20-25-red"/>',
            '<img alt="" src="https://img.shields.io/badge/days%20completed-25-green"/>',
            '<img alt="" src="https://img.shields.io/badge/stars%20-50-blue" />',
        ]
        arr.append(f"[{year} Puzzles]({complete_path}) <p>{' '.join(badges)}</p>")

    return '\n\n'.join(arr)


with open(join(docs_path, 'index.md'), 'r') as rf:
    index_data = rf.read()

    index_data = index_data.replace('{{previous_years}}', previous_years())
    index_data = index_data.replace('{{current_year_outputs}}', f'### {curr_year} Puzzle Outputs')
    index_data = index_data.replace('{{docker_command}}', f'make year={curr_year} run-year-puzzles')

    with open(join(root_path, 'README.md'), 'w') as wf:
        wf.writelines(markdown(index_data, extensions=[markdown_include]))

with open(join(docs_path, 'year.md'), 'r') as rf:
    year_data = rf.read()

    year_data = year_data.replace('{{heading}}', f'# Advent of Code {curr_year}')
    year_data = year_data.replace('{{docker_command}}', f'make year={curr_year} run-year-puzzles')

    with open(join(year_path, 'README.md'), 'w') as wf:
        wf.writelines(markdown(year_data, extensions=[markdown_include]))
