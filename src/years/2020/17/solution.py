
from collections import defaultdict
from typing import Dict, List, Tuple

from aocpuzzle import AoCPuzzle


class Puzzle17(AoCPuzzle):

    def common(self, input_data: List[str]) -> None:
        self.directions = [-1, 0, 1]
        self.pocket: Dict[Tuple[int, int, int, int], bool] = defaultdict(lambda: False)

        for y, line in enumerate(input_data):
            for x, state in enumerate(line):
                self.pocket[x, y, 0, 0] = state == '#'

    def neighbors(self, x: int, y: int, z: int, w: int) -> List[Tuple[int, int, int, int]]:
        return [
            (x + nx, y + ny, z + nz, w + nw)
            for nx in self.directions
            for ny in self.directions
            for nz in self.directions
            for nw in self.directions
            if (nx, ny, nz, nw) != (0, 0, 0, 0)
        ]

    def active_neighbors(self, x: int, y: int, z: int, w: int) -> int:
        return sum(self.pocket[coord] for coord in self.neighbors(x, y, z, w))

    def minmax_coords(self) -> List[int]:
        keys = self.pocket.keys()

        min_x = min(keys, key=lambda k: k[0])[0]
        max_x = max(keys, key=lambda k: k[0])[0]
        min_y = min(keys, key=lambda k: k[1])[1]
        max_y = max(keys, key=lambda k: k[1])[1]
        min_z = min(keys, key=lambda k: k[2])[2]
        max_z = max(keys, key=lambda k: k[2])[2]
        min_w = min(keys, key=lambda x: x[3])[3]
        max_w = max(keys, key=lambda x: x[3])[3]

        return [min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w]

    def cycle(self) -> None:
        new_pocket = defaultdict(lambda: False)

        [min_x, max_x, min_y, max_y, min_z, max_z, _, _] = self.minmax_coords()

        for z in range(min_z - 1, max_z + 2):
            for y in range(min_y - 1, max_y + 2):
                for x in range(min_x - 1, max_x + 2):
                    is_active = self.pocket[x, y, z, 0]
                    num_active_neighbors = self.active_neighbors(x, y, z, 0)

                    if is_active is True:
                        new_pocket[x, y, z, 0] = num_active_neighbors in [2, 3]
                    else:
                        new_pocket[x, y, z, 0] = num_active_neighbors == 3

        self.pocket = new_pocket

    def cycle2(self) -> None:
        new_pocket = defaultdict(lambda: False)

        [min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w] = self.minmax_coords()

        for w in range(min_w - 1, max_w + 2):
            for z in range(min_z - 1, max_z + 2):
                for y in range(min_y - 1, max_y + 2):
                    for x in range(min_x - 1, max_x + 2):
                        is_active = self.pocket[x, y, z, w]
                        num_active_neighbors = self.active_neighbors(x, y, z, w)

                        if is_active is True:
                            new_pocket[x, y, z, w] = num_active_neighbors in [2, 3]
                        else:
                            new_pocket[x, y, z, w] = num_active_neighbors == 3

        self.pocket = new_pocket

    def part1(self, input_data: List[str]) -> int:
        for _ in range(6):
            self.cycle()
        return sum(self.pocket.values())

    def part2(self, input_data: List[str]) -> int:
        for _ in range(6):
            self.cycle2()
        return sum(self.pocket.values())

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            '.#.',
            '..#',
            '###',
        ]
        self.common(tests)
        assert self.part1(tests) == 112

        self.common(tests)
        assert self.part2(tests) == 848

        self.common(input_data)
        assert self.part1(input_data) == 298
        self.common(input_data)
        assert self.part2(input_data) == 1792

        return 2
