

from collections import defaultdict
from math import inf
from typing import Union

from aocpuzzle import AoCPuzzle

position_tuple = tuple[int, int]


class Puzzle12(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.height_map: dict[position_tuple, int] = defaultdict()
        self.all_lowest_elevation_pos = set()

        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        for row, line in enumerate(input_data):
            for col, elevation in enumerate(line):
                pos = (row, col)

                if elevation == 'S':
                    elevation = 'a'
                    self.start_pos = pos
                if elevation == 'E':
                    elevation = 'z'
                    self.destination_pos = pos

                if elevation == 'a':
                    self.all_lowest_elevation_pos.add(pos)

                self.height_map[pos] = abs(ord(elevation) - ord('a'))

    def pos_inside_grid(self, row: int, col: int) -> bool:
        return (row, col) in self.height_map

    def get_valid_neighbors(self, pos: position_tuple, visited_positions: set[position_tuple]) -> list[position_tuple]:
        valid_neighbors = []

        for dx, dy in self.directions:
            nx, ny = pos[0] + dx, pos[1] + dy
            neighbor_pos = (nx, ny)

            if self.pos_inside_grid(nx, ny) and neighbor_pos not in visited_positions:
                if self.height_map[neighbor_pos] <= self.height_map[pos] + 1:
                    valid_neighbors.append(neighbor_pos)

        return valid_neighbors

    def shortest_path(self, start_pos: position_tuple) -> Union[int, float]:
        positions_to_visit: list[tuple[position_tuple, int]] = [(start_pos, 0)]

        visited_positions: set[position_tuple] = set([start_pos])

        total_steps = inf

        while len(positions_to_visit) > 0:
            current_pos, steps_to_pos = positions_to_visit.pop(0)

            if current_pos == self.destination_pos:
                total_steps = steps_to_pos
                break

            for neighbor in self.get_valid_neighbors(current_pos, visited_positions):
                positions_to_visit.append((neighbor, steps_to_pos + 1))
                visited_positions.add(neighbor)

        return total_steps

    def part1(self) -> int:
        return int(self.shortest_path(self.start_pos))

    def part2(self) -> int:
        return int(min([self.shortest_path(start_pos)for start_pos in self.all_lowest_elevation_pos]))

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'Sabqponm',
                    'abcryxxl',
                    'accszExk',
                    'acctuvwj',
                    'abdefghi',
                ],
                'part1': 31,
                'part2': 29,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 456
        self.common(input_data)
        assert self.part2() == 454

        return len(tests) + 1
