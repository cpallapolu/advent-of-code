from argparse import ArgumentParser
from datetime import date
from json import loads
from os import system as o_system
from os.path import abspath, dirname, isfile, join
from pathlib import Path
from platform import system as p_system
from shutil import copy
from sys import exit
from time import time
from traceback import print_exc

from tabulate import tabulate

from load_year import load_year

RED = '\033[91m'
PURPLE = '\033[95m'
RESET = '\033[0m'
GREEN = '\033[92m'
BOLD = '\033[1m'

base_template = """
from aocpuzzle import AoCPuzzle

from typing import Any


class Puzzle{0}(AoCPuzzle):
    def common(self, input_data: Any) -> None:
        print('day{0} common in day{0}')

    def part1(self, input_data: Any) -> int:
        print('day{0} part 1 in day{0}')
        return {0}

    def part2(self, input_data: Any) -> int:
        print('day{0} part 2 in day{0}')
        return {0}

    def test_cases(self, input_data: Any) -> int:
        print('day{0} test_cases in day{0}')
        return 2
"""


def main(year: int, puzzle: int, all_puzzles: bool, cache: bool) -> None:
    src_path = dirname(abspath(__file__))
    year_path = abspath(join(src_path, f'years/{year}'))
    root_path = abspath(join(src_path, '../'))

    settings_path = join(year_path, 'settings.json')
    settings_default_path = join(src_path, 'settings.default.json')

    if isfile(settings_path):
        with open(settings_path, 'r') as s:
            settings = loads(''.join(s.readlines()))
    else:
        copy(settings_default_path, settings_path)
        print(f'\nPlease fill in {settings_path} first!')
        exit(1)

    session = settings['session']

    puzzles_to_run = [puzzle]

    if all_puzzles is True:
        puzzles_to_run = [day for day in range(1, 26)]

    puzzle_outputs = [
        [
            '#', 'Part 1', 'Part 1 Time',
            'Part 2', 'Part 2 Time', 'Tests', 'Tests Time',
        ],
    ]
    puzzles = load_year(year)

    for day in [f'{d:02d}' for d in puzzles_to_run]:
        puzzle_class = f'Puzzle{day}'

        if puzzle_class in puzzles:
            print(f'Attempting to execute AoC puzzle {day}...: ', end='', flush=True)

            start_time = time()
            try:
                puzzle_instance = puzzles[puzzle_class](year, day, session)
                puzzle_instance.execute(cache)

                puzzle_outputs.append(puzzle_instance.results)
                end_time = f'{((time() - start_time) * 1000):.3f}'
                print(f'{BOLD}{GREEN} Successful{RESET} in {BOLD}{PURPLE}{end_time} ms{RESET}')

            except ConnectionError:
                print(f'{BOLD}{GREEN} Failed {RESET}')
            except Exception:
                print(f'{BOLD}{GREEN} Failed {RESET}')
                print_exc()
                print()
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

        if all_puzzles is True:
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
    year = date.today().year
    year_choices = [year for year in range(2020, year + 1)]

    day = date.today().day
    day_choices = [day for day in range(1, 26)]

    parser = ArgumentParser()

    parser.add_argument(
        '--year', required=False, default=year, type=int, choices=year_choices, help='year to run',
    )
    parser.add_argument(
        '--puzzle', default=0, type=int, choices=day_choices, help='puzzle to run', metavar='num',
    )
    parser.add_argument(
        '--all_puzzles', default=False, type=bool, help='run all puzzles', metavar='bool',
    )
    parser.add_argument(
        '--cache', default=False, type=bool, help='retrun cache results of puzzles', metavar='bool',
    )
    args = parser.parse_args()

    if args.puzzle == 0:
        args.all_puzzles = True

    main(args.year, args.puzzle, args.all_puzzles, args.cache)
