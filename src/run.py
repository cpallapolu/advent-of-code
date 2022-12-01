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


class Puzzle{0}(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        print('day{0} common in day{0}')

    def part1(self) -> int:
        print('day{0} part 1 in day{0}')
        return 1

    def part2(self) -> int:
        print('day{0} part 2 in day{0}')
        return 2

    def test_cases(self, input_data: list[str]) -> int:
        print('day{0} test_cases in day{0}')
        tests: list[dict] = [
            {{
                'input_data': [],
                'part1': 1,
                'part2': 2,
            }},
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        return len(tests) + 1
"""


def main(year: int, puzzle: int, all_puzzles: bool, cache: bool) -> None:
    src_path = dirname(abspath(__file__))
    year_path = abspath(join(src_path, f'years/{year}'))
    root_path = abspath(join(src_path, '../'))

    settings_path = join(year_path, 'settings.json')
    settings_default_path = join(src_path, 'settings.default.json')
    output_table_path = join(root_path, './docs/output_table.md')

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
        puzzles_to_run = [day for day in range(1, min(puzzle + 1, 26))]

    puzzle_outputs = [
        [
            '#', 'Puzzle Name', 'Part 1', 'Part 1 Time',
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
            puzzle_dir = join(year_path, f'{day}')
            puzzle_solution = join(year_path, f'{day}/solution.py')

            puzzle_path = Path(puzzle_dir)
            puzzle_path.mkdir()

            with open(puzzle_solution, 'w') as f:
                f.writelines(template)

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

        with open(join(root_path, output_table_path), 'w') as f:
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
    curr_year = date.today().year
    year_choices = [year for year in range(2020, curr_year + 1)]

    day = date.today().day
    day_choices = [day for day in range(1, 26)]

    parser = ArgumentParser(description='Advent of Code')

    parser.add_argument('--year', default=curr_year, type=int, choices=year_choices, help='year to run', metavar='num')
    parser.add_argument('--puzzle', default=day, type=int, choices=day_choices, help='puzzle to run', metavar='num')
    parser.add_argument('--all_puzzles', default=False, action='store_true', help='run all puzzles')
    parser.add_argument('--cache', default=False, action='store_true', help='return cache results of puzzles')

    args = parser.parse_args()

    if args.cache is True:
        args.all_puzzles = True

    main(args.year, args.puzzle, args.all_puzzles, args.cache)
