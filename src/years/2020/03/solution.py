from math import prod
from typing import List

from aocpuzzle import AoCPuzzle


class Puzzle03(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.tree_map, self.rows, self.cols = input_data, len(input_data), len(input_data[0])

    def count_trees(self, right: int, down: int) -> int:
        row, col, ans = 0, 0, 0

        while True:
            row += down

            if row >= self.rows:
                break

            col = (col + right) % self.cols

            ans += self.tree_map[row][col] == '#'

        return ans

    def part1(self) -> int:
        return self.count_trees(3, 1)

    def part2(self) -> int:
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

        self.common(geology_map)
        assert self.part1() == 7
        self.common(input_data)
        assert self.part1() == 218

        self.common(geology_map)
        assert self.part2() == 336
        self.common(input_data)
        assert self.part2() == 3847183340

        return 2
