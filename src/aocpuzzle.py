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
            print(f"\nInput already downloded to '{self.input_filename}' path.")

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
            self.input_data = [x.replace('\n', '') for x in f.readlines()]

            if len(self.input_data) == 1:
                self.input_data = self.input_data[0]

            self.input_data = self.post_process_input_data(self.input_data)

    def delete_output(self):
        if isfile(self.output_filename):
            remove(self.output_filename)

    def execute(self):
        self.download_input()
        self.load_input()
        self.delete_output()

        with open(self.output_filename, 'w') as output_file:
            def print_fc(text):
                print(text, file=output_file)

            self.common(self.input_data)

            start_time = time()

            self.part1_res = self.part1(self.input_data)

            print_fc('\nPart 1:\n============================================')
            print_fc(f'Result: {self.part1_res}')

            self.part1_exec_time = f'{((time() - start_time) * 1000):.3f} ms'
            print_fc(f'Execution time: {self.part1_exec_time}')

            start_time = time()

            self.part2_res = self.part2(self.input_data)

            print_fc('\nPart 2:\n============================================')
            print_fc(f'Result: {self.part2_res}')

            self.part2_exec_time = f'{((time() - start_time) * 1000):.3f} ms'
            print_fc(f'Execution time: {self.part2_exec_time}')

            self.num_test_cases = self.test_cases(self.input_data)

    def post_process_input_data(self, input_data: Any) -> Any:
        return input_data

    def common(self, input_data: Any) -> None:
        pass

    def part1(self):
        pass

    def part2(self):
        pass

    def test_cases(self):
        pass
