from os import getcwd, remove
from os.path import isfile, join
from time import time
from typing import Any, List

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

    def execute(self, is_cache: bool):
        self.download_input()
        self.load_input()

        self.results: List[str] = []

        if is_cache is False:
            self.delete_output()

            self.results.append(str(self.day_number))

            for part in range(1, 3):
                start_time = time()

                self.common(self.input_data)

                part_func = getattr(self, f'part{part}')
                self.results.append(str(part_func(self.input_data)))
                self.results.append(f'{((time() - start_time) * 1000):.3f} ms')

            start_time = time()
            self.results.append(str(self.test_cases(self.input_data)))
            self.results.append(f'{((time() - start_time) * 1000):.3f} ms')
        else:
            self.results = self.get_cache_results()

        with open(self.output_filename, 'w') as output_file:
            print('|'.join(self.results), file=output_file)
            print('\nPart 1:\n============================================', file=output_file)
            print(f'Result: {self.results[1]}', file=output_file)
            print(f'Execution time: {self.results[2]}', file=output_file)
            print('\nPart 2:\n============================================', file=output_file)
            print(f'Result: {self.results[3]}', file=output_file)
            print(f'Execution time: {self.results[4]}', file=output_file)

    def get_cache_results(self) -> List[str]:
        results: List[str] = []

        with open(self.output_filename, 'r') as output_file:
            results = output_file.readline().rstrip().split('|')

        return results

    def common(self, input_data: Any) -> None:
        pass

    def part1(self, input_data: Any) -> Any:
        pass

    def part2(self, input_data: Any) -> Any:
        pass

    def test_cases(self, input_data: Any) -> Any:
        pass
