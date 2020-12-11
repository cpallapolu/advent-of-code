from os import getcwd, remove
from os.path import isfile, join
from time import time
from typing import Any

from requests import get


class AoCPuzzle:
    def __init__(self, year: int, day_number: int, session: str) -> None:
        self.year = year
        self.day_number = day_number
        self.session = session

        self.input_filename = join(getcwd(), f'src/puzzles/{self.day_number}/input')
        self.output_filename = join(getcwd(), f'src/puzzles/{self.day_number}/output')

        self.input_data: Any = {}

    def download_input(self) -> None:
        if isfile(self.input_filename):
            return

        print(f'Downloading input file for day {self.day_number}...')
        dl_url = f'https://adventofcode.com/{self.year}/day/{int(str(self.day_number))}/input'

        response = get(dl_url, cookies={'session': self.session})
        status_code, text = response.status_code, response.text

        if status_code == 200:
            self.input_data = text

            with open(self.input_filename, 'w') as f:
                f.write(text)
        else:
            raise ConnectionError(
                f'Unable to download input data. Error code {status_code} : {text}',
            )

    def load_input(self) -> None:
        with open(self.input_filename, 'r') as f:
            self.input_data = [line.strip() for line in f.readlines()]

            if len(self.input_data) == 1:
                self.input_data = self.input_data[0]

    def delete_output(self):
        if isfile(self.output_filename):
            remove(self.output_filename)

    def execute(self):
        self.download_input()
        self.load_input()
        self.delete_output()

        self.results = [self.day_number]

        for part in range(1, 3):
            start_time = time()

            self.common(self.input_data)

            part_func = getattr(self, f'part{part}')
            self.results.append(part_func(self.input_data))
            self.results.append(f'{((time() - start_time) * 1000):.3f} ms')

        start_time = time()
        self.results.append(self.test_cases(self.input_data))
        self.results.append(f'{((time() - start_time) * 1000):.3f} ms')

        with open(self.output_filename, 'w') as output_file:
            print('\nPart 1:\n============================================', file=output_file)
            print(f'Result: {self.results[0]}', file=output_file)
            print(f'Execution time: {self.results[1]}', file=output_file)
            print('\nPart 2:\n============================================', file=output_file)
            print(f'Result: {self.results[2]}', file=output_file)
            print(f'Execution time: {self.results[3]}', file=output_file)

    def common(self, input_data: Any) -> None:
        pass

    def part1(self, input_data: Any) -> Any:
        pass

    def part2(self, input_data: Any) -> Any:
        pass

    def test_cases(self, input_data: Any) -> Any:
        pass
