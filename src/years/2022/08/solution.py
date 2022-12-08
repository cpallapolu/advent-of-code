

from math import prod

from aocpuzzle import AoCPuzzle


class Puzzle08(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.grid: list[list[int]] = [[int(height) for height in line] for line in input_data]
        self.grid_cols: list[list[int]] = list(map(list, zip(*self.grid)))
        self.max_row = len(self.grid) - 1
        self.max_col = len(self.grid[0]) - 1

    def get_tree_lines(self, row: int, col: int) -> list[list[int]]:
        return [
            self.grid_cols[col][row - 1::-1],
            self.grid_cols[col][row + 1:],
            self.grid[row][col - 1::-1],
            self.grid[row][col + 1:],
        ]

    def is_edge(self, row: int, col: int) -> bool:
        return True if row == 0 or row == self.max_row or col == 0 or col == self.max_col else False

    def is_visible(self, height: int, row: int, col: int) -> int:
        if self.is_edge(row, col):
            return 1

        return any(
            all(tree_height < height for tree_height in tree_line)
            for tree_line in self.get_tree_lines(row, col)
        )

    def scenic_score(self, height: int, row: int, col: int) -> int:
        if self.is_edge(row, col):
            return 0

        return prod([
            next((idx for idx, tree_height in enumerate(tree_line, start=1) if tree_height >= height), len(tree_line))
            for tree_line in self.get_tree_lines(row, col)
        ])

    def part1(self) -> int:
        return sum(
            self.is_visible(self.grid[row][col], row, col)
            for row in range(self.max_row + 1)
            for col in range(self.max_col + 1)
        )

    def part2(self) -> int:
        return max(
            self.scenic_score(self.grid[row][col], row, col)
            for row in range(self.max_row + 1)
            for col in range(self.max_col + 1)
        )

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '30373',
                    '25512',
                    '65332',
                    '33549',
                    '35390',
                ],
                'part1': 21,
                'part2': 8,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 1717
        self.common(input_data)
        assert self.part2() == 321975

        return len(tests) + 1
