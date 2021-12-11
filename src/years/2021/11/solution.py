
from collections import defaultdict
from itertools import product

from aocpuzzle import AoCPuzzle

ENERGY_LEVEL_TYPE = dict[tuple[int, int], int]


class Puzzle11(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.energy_levels: ENERGY_LEVEL_TYPE = defaultdict(int)
        for row_idx, row in enumerate(input_data):
            for col_idx, level in enumerate(row):
                self.energy_levels[(row_idx, col_idx)] = int(level)

    def get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        neighbors = []

        for x, y in product([-1, 0, 1], repeat=2):
            new_row, new_col = row + x, col + y

            if (new_row, new_col) in self.energy_levels:
                neighbors.append((new_row, new_col))

        return neighbors

    def flash(self, row: int, col: int) -> None:
        self.flashes[(row, col)] = True

        for n_row, n_col in self.get_neighbors(row, col):
            self.curr_energy_levels[(n_row, n_col)] += 1

            if (n_row, n_col) not in self.flashes and self.curr_energy_levels[(n_row, n_col)] > 9:
                self.flash(n_row, n_col)

    def step(self) -> None:
        self.curr_energy_levels: ENERGY_LEVEL_TYPE = defaultdict(int)
        self.flashes: ENERGY_LEVEL_TYPE = defaultdict(int)

        for row, col in self.energy_levels.keys():
            self.curr_energy_levels[(row, col)] += self.energy_levels[(row, col)] + 1

            if self.curr_energy_levels[(row, col)] > 9:
                self.flash(row, col)

        self.energy_levels = {
            (row, col): 0 if level > 9 else level
            for (row, col), level in self.curr_energy_levels.items()
        }

    def part1(self) -> int:
        total_flashes = 0

        for _ in range(100):
            self.step()

            total_flashes += sum(
                level == 0
                for level in self.energy_levels.values()
            )

        return total_flashes

    def part2(self) -> int:
        step = 0

        while all(level == 0 for level in self.energy_levels.values()) is False:
            self.step()

            step += 1

        return step

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '11111',
                    '19991',
                    '19191',
                    '19991',
                    '11111',
                ],
                'part1': 259,
                'part2': 6,
            },
            {
                'input_data': [
                    '5483143223',
                    '2745854711',
                    '5264556173',
                    '6141336146',
                    '6357385478',
                    '4167524645',
                    '2176841721',
                    '6882881134',
                    '4846848554',
                    '5283751526',
                ],
                'part1':1656,
                'part2': 195,
            },

        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 1642
        self.common(input_data)
        assert self.part2() == 320

        return len(tests) + 1
