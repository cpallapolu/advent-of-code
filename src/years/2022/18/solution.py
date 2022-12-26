

from queue import Queue

from aocpuzzle import AoCPuzzle
from years.utils.geo import Position3D

NEIGHBORS = [
    Position3D(1, 0, 0),
    Position3D(-1, 0, 0),
    Position3D(0, 1, 0),
    Position3D(0, -1, 0),
    Position3D(0, 0, 1),
    Position3D(0, 0, -1),
]


class Puzzle18(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.droplet_cubes = set()

        for line in input_data:
            x, y, z = map(int, line.split(','))
            self.droplet_cubes.add(Position3D(x + 1, y + 1, z + 1))

    def part1(self) -> int:
        return sum([
            (droplet_cube + neighbor) not in self.droplet_cubes
            for droplet_cube in self.droplet_cubes
            for neighbor in NEIGHBORS
        ])

    def inside_boundary(self, neighbor: Position3D) -> bool:
        return (
            neighbor.x >= 0
            and neighbor.y >= 0
            and neighbor.z >= 0
            and neighbor.x < self.max_x
            and neighbor.y < self.max_y
            and neighbor.z < self.max_z
        )

    def part2(self) -> int:
        outside = set()

        self.max_x = max(cube.x for cube in self.droplet_cubes) + 2
        self.max_y = max(cube.y for cube in self.droplet_cubes) + 2
        self.max_z = max(cube.z for cube in self.droplet_cubes) + 2

        queue: Queue[Position3D] = Queue()

        start = Position3D(0, 0, 0)
        outside.add(start)
        queue.put(start)

        while queue.empty() is False:
            cur = queue.get()
            for neighbor in NEIGHBORS:
                next_neighbor = cur + neighbor
                inside_boundary = self.inside_boundary(next_neighbor)

                if inside_boundary and next_neighbor not in self.droplet_cubes and next_neighbor not in outside:
                    outside.add(next_neighbor)
                    queue.put(next_neighbor)

        return sum([
            (droplet_cube + neighbor) not in self.droplet_cubes and (droplet_cube + neighbor) in outside
            for droplet_cube in self.droplet_cubes
            for neighbor in NEIGHBORS
        ])

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '2,2,2',
                    '1,2,2',
                    '3,2,2',
                    '2,1,2',
                    '2,3,2',
                    '2,2,1',
                    '2,2,3',
                    '2,2,4',
                    '2,2,6',
                    '1,2,5',
                    '3,2,5',
                    '2,1,5',
                    '2,3,5',
                ],
                'part1': 64,
                'part2': 58,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 3326
        self.common(input_data)
        assert self.part2() == 1996

        return len(tests) + 1
