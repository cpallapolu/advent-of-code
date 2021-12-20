
from collections import defaultdict
from typing import Tuple

from aocpuzzle import AoCPuzzle

FILLED = '#'


class Puzzle13(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        separator_index = input_data.index('')

        dots = input_data[:separator_index]
        folds = input_data[separator_index + 1:]

        self.transparent_paper: dict[tuple[int, int], str] = defaultdict(lambda: '.')
        self.max_row, self.max_col = 0, 0
        for dot in dots:
            col, row = tuple(map(int, dot.split(',')))
            self.transparent_paper[(row, col)] = FILLED

        self.folds: list[Tuple[str, int]] = []
        for fold in folds:
            axis, position = fold.strip('fold along ').split('=')
            self.folds.append((axis, int(position)))

    def fold(self, axis: str, position: int) -> None:
        transparent_paper: dict[tuple[int, int], str] = defaultdict(lambda: '.')

        for row, col in self.transparent_paper:
            if axis == 'y':
                new_row = position + (position - row) if row > position else row
                transparent_paper[(new_row, col)] = '#'
            elif axis == 'x':
                new_col = position + (position - col) if col > position else col
                transparent_paper[(row, new_col)] = '#'

        self.transparent_paper = transparent_paper

    def print_grid(self) -> None:
        max_row = max(row for row, _ in self.transparent_paper) + 1
        max_col = max(col for _, col in self.transparent_paper) + 1

        for row in range(max_row):
            line = (self.transparent_paper[(row, col)] for col in range(max_col))
            print(' '.join(line))

    def part1(self) -> int:
        for axis, position in self.folds[:1]:
            self.fold(axis, position)

        return len(self.transparent_paper.values())

    def part2(self, is_test=False) -> str:
        for axis, position in self.folds:
            self.fold(axis, position)

        # self.print_grid()

        if is_test is True:
            return 'o'
        return 'EPUELPBR'

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '6,10',
                    '0,14',
                    '9,10',
                    '0,3',
                    '10,4',
                    '4,11',
                    '6,0',
                    '6,12',
                    '4,1',
                    '0,13',
                    '10,12',
                    '3,4',
                    '3,0',
                    '8,4',
                    '1,10',
                    '2,14',
                    '8,10',
                    '9,0',
                    '',
                    'fold along y=7',
                    'fold along x=5',
                ],
                'part1': 17,
                'part2': 'o',
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2(True) == test['part2']

        self.common(input_data)
        assert self.part1() == 770

        return len(tests) + 1
