
from importlib import import_module
from inspect import isclass
from os import listdir
from os.path import abspath, dirname, join
from typing import Any, Dict

ignore_files = ['__', 'settings', 'README', 'OUTPUTS_TABLE']


def is_ignored_file(f):
    return all([f.startswith(ignore_file) is False for ignore_file in ignore_files])


def load_year(year: int) -> Dict[str, Any]:
    puzzles = {}

    years_path = abspath(join(dirname(abspath(__file__)), f'years/{year}'))
    solutions = [
        f'{f}.solution'
        for f in listdir(years_path)
        if is_ignored_file(f) is True
    ]

    for solution in solutions:
        module = import_module('.'.join(['years', str(year), solution]))

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if attribute_name.startswith('Puzzle') and isclass(attribute):
                puzzles[attribute_name] = attribute

    return puzzles
