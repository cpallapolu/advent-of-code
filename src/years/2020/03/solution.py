from math import prod
from typing import List

from aocpuzzle import AoCPuzzle


class Puzzle03(AoCPuzzle):
    def count_trees(self, right: int, down: int) -> int:
        row, col, ans = 0, 0, 0

        while True:
            row += down

            if row >= self.rows:
                break

            col = (col + right) % self.cols

            ans += self.input_data[row][col] == '#'

        return ans

    def part1(self, input_data: List[str]) -> int:
        self.input_data, self.rows, self.cols = input_data, len(input_data), len(input_data[0])

        return self.count_trees(3, 1)

    def part2(self, input_data: List[str]) -> int:
        self.input_data, self.rows, self.cols = input_data, len(input_data), len(input_data[0])

        return prod([
            self.count_trees(right, down)
            for right, down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        ])

    def test_cases(self, input_data: List[str]) -> int:
        geology_map = [
            '..##.......',
            '#...#...#..',
            '.#....#..#.',
            '..#.#...#.#',
            '.#...##..#.',
            '..#.##.....',
            '.#.#.#....#',
            '.#........#',
            '#.##...#...',
            '#...##....#',
            '.#..#...#.#',
        ]

        assert self.part1(geology_map) == 7
        assert self.part1(input_data) == 218

        assert self.part2(geology_map) == 336
        assert self.part2(input_data) == 3847183340

        return 2
