from datetime import date
from json import loads
from os import system as o_system
from os.path import abspath, dirname, isfile, join
from pathlib import Path
from platform import system as p_system
from shutil import copy
from sys import argv, exit, stderr
from traceback import print_exc

from tabulate import tabulate

import puzzles

base_template = """
from aocpuzzle import AoCPuzzle

from typing import Any


class Puzzle{0}(AoCPuzzle):
    def part1(self, input_data: Any) -> Any:
        print('day{0} part 1 in day{0}')
        return 'day{0}-part1'

    def part2(self, input_data: Any) -> Any:
        print('day{0} part 2 in day{0}')
        return 'day{0}-part2'

    def test_cases(self, input_data: Any) -> int:
        print('day{0} test_cases in day{0}')
        return 2
"""


def main():
    args = argv
    puzzle_number = 1
    run_all_puzzles = False
    curr_puzzle = date.today().day

    src_path = dirname(abspath(__file__))
    root_path = abspath(join(src_path, '../'))

    settings_path = join(src_path, 'settings.json')
    settings_default_path = join(src_path, 'settings.default.json')

    if len(args) > 1:
        input_puzzle = args[1]

        if input_puzzle == 'all':
            run_all_puzzles = True
        else:
            puzzle_number = int(args[1])
    else:
        puzzle_number = curr_puzzle

    if puzzle_number < 1 or puzzle_number > 25:
        print('\nGiven Puzzle is out of range 1-25.\n')
        exit(1)

    if isfile(settings_path):
        with open(settings_path, 'r') as s:
            settings = loads(''.join(s.readlines()))
    else:
        copy(settings_default_path, settings_path)
        print('\nPlease fill in settings.json first!')
        exit(1)

    session = settings['session']
    year = settings['year']

    puzzles_to_run = [puzzle_number]

    last_puzzle_num = curr_puzzle + 1 if curr_puzzle < 26 else 26

    if run_all_puzzles:
        puzzles_to_run = [day for day in range(1, last_puzzle_num)]

    puzzle_outputs = [
        [
            'Puzzle #',
            'Part 1', 'Part 1 Time',
            'Part 2', 'Part 2 Time',
            'Tests #', 'Tests Time',
        ],
    ]

    for day in [f'{d:02d}' for d in puzzles_to_run]:
        puzzle_class = f'Puzzle{day}'

        if puzzle_class in dir(puzzles):
            print(f'Attempting to execute AoC puzzle {day}...')

            try:
                puzzle_class = getattr(puzzles, f'Puzzle{day}')
                puzzle_instance = puzzle_class(year, day, session)
                puzzle_instance.execute()

                puzzle_outputs.append(puzzle_instance.results)
            except ConnectionError as ce:
                print(ce, file=stderr)
            except Exception as e:
                print(e, file=stderr)
                print_exc()
        else:
            template = base_template.format(day)
            puzzle_dir = join(src_path, 'puzzles/{}'.format(day))
            puzzle_solution = join(src_path, 'puzzles/{}/solution.py'.format(day))

            puzzle_path = Path(puzzle_dir)
            puzzle_path.mkdir()

            with open(puzzle_solution, 'w') as f:
                f.writelines(template.format(day))

            print(f'\nClass for day {day} created. Happy Coding!!\n')
            exit(1)

    if len(puzzle_outputs) > 1:
        table = tabulate(
            puzzle_outputs,
            headers='firstrow',
            tablefmt='pretty',
            numalign='left',
            stralign='left',
        )

        if p_system() != 'Windows':
            o_system('clear')

        print(table)

        with open(join(root_path, 'docs/output_table.md'), 'w') as f:
            f.writelines(
                tabulate(
                    puzzle_outputs,
                    headers='firstrow',
                    tablefmt='html',
                    numalign='left',
                    stralign='left',
                ),
            )


if __name__ == '__main__':
    """Driver code."""
    main()
