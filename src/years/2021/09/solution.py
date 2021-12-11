
from math import prod

from aocpuzzle import AoCPuzzle


class Puzzle09(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.heat_map = {
            (row_idx, col_idx): int(height)
            for row_idx, row in enumerate(input_data)
            for col_idx, height in enumerate(row)
        }

    def get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        neighbors = []

        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + x, col + y

            if (new_row, new_col) in self.heat_map:
                neighbors.append((new_row, new_col))

        return neighbors

    def get_low_points(self) -> list[tuple[int, int]]:
        low_points = []
        for [row, col], height in self.heat_map.items():
            all_low_points = all(
                self.heat_map[(row, col)] < self.heat_map[neighbor]
                for neighbor in self.get_neighbors(row, col)
            )
            if all_low_points is True:
                low_points.append((row, col))

        return low_points

    def part1(self) -> int:
        return sum([
            self.heat_map[low_point] + 1
            for low_point in self.get_low_points()
        ])

    def part2(self) -> int:
        basin_sizes = []

        for low_point in self.get_low_points():
            points_in_basin = set([low_point])
            can_flow_into = [low_point]

            while len(can_flow_into) > 0:
                row, col = can_flow_into.pop()

                for neighbour in self.get_neighbors(row, col):
                    neighbour_height = self.heat_map.get(neighbour, 0)

                    if neighbour_height > self.heat_map[(row, col)] and neighbour_height != 9:

                        points_in_basin.add(neighbour)
                        can_flow_into.append(neighbour)

            basin_sizes.append(len(points_in_basin))

        return prod(sorted(basin_sizes)[-3:])

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '2199943210',
                    '3987894921',
                    '9856789892',
                    '8767896789',
                    '9899965678',
                ],
                'part1': 15,
                'part2': 1134,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 572
        self.common(input_data)
        assert self.part2() == 847044

        return len(tests) + 1
