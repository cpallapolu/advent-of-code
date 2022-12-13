from os import getcwd, remove
from os.path import isfile, join
from time import time
from typing import Any, List

from bs4 import BeautifulSoup
from markdownify import markdownify
from requests import get


class AoCPuzzle:
    def __init__(self, year: int, day_number: int, session: str) -> None:
        self.year = year
        self.day_number = day_number
        self.session = session

        self.readme_filename = join(getcwd(), f'src/years/{year}/{self.day_number}/README.md')
        self.input_filename = join(getcwd(), f'src/years/{year}/{self.day_number}/input')
        self.output_filename = join(getcwd(), f'src/years/{year}/{self.day_number}/output')

        self.input_data: Any = {}

    def download_problem_statement(self) -> None:
        if isfile(self.readme_filename):
            with open(self.readme_filename, 'r') as f:
                if '## Part Two' in f.read():
                    return

        print(f'Downloading problem statement for day {self.day_number}...')
        dl_url = f'https://adventofcode.com/{self.year}/day/{int(str(self.day_number))}'

        response = get(dl_url, cookies={'session': self.session})
        status_code, text = response.status_code, response.text

        if status_code == 200:
            self.input_data = text

            soup = BeautifulSoup(text, 'html.parser')
            articles = soup.find_all('article')

            with open(self.readme_filename, 'w') as f:
                f.write(markdownify(''.join(map(str, articles))))
        else:
            raise ConnectionError(
                f'Unable to download input data. Error code {status_code} : {text}',
            )

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
        self.download_problem_statement()
        self.download_input()
        self.load_input()

        self.results: List[str] = []

        if is_cache is False:
            self.results.append(str(self.day_number))

            with open(self.readme_filename, 'r')as readme_file:
                full_name = readme_file.readline()
                colon_idx = full_name.index(':')
                self.results.append(full_name[colon_idx + 1:].strip())

            start_time = time()
            self.results.append(str(self.test_cases(self.input_data)))
            self.results.append(f'{((time() - start_time) * 1000):.3f} ms')

            for part in range(1, 3):
                start_time = time()

                self.common(self.input_data)

                part_func = getattr(self, f'part{part}')
                self.results.append(str(part_func()))
                self.results.append(f'{((time() - start_time) * 1000):.3f} ms')

            self.results = self.results[:2] + self.results[4:] + self.results[2:4]
        else:
            self.results = self.get_cache_results()

        with open(self.output_filename, 'w') as output_file:
            print('|'.join(self.results), file=output_file)
            print('\nPart 1:\n============================================', file=output_file)
            print(f'Result: {self.results[2]}', file=output_file)
            print(f'Execution time: {self.results[3]}', file=output_file)
            print('\nPart 2:\n============================================', file=output_file)
            print(f'Result: {self.results[4]}', file=output_file)
            print(f'Execution time: {self.results[5]}', file=output_file)

    def get_cache_results(self) -> List[str]:
        results: List[str] = []

        with open(self.output_filename, 'r') as output_file:
            results = output_file.readline().rstrip().split('|')

        return results

    def common(self, input_data: Any) -> None:
        pass

    def part1(self) -> Any:
        pass

    def part2(self) -> Any:
        pass

    def test_cases(self, input_data: Any) -> Any:
        pass
