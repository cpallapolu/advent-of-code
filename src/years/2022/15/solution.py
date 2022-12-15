

from re import findall

from z3 import If, Int, Solver

from aocpuzzle import AoCPuzzle


class Puzzle15(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.observations = [
            list(map(int, findall(r'-?\d+', observation)))
            for observation in input_data
        ]

    def part1(self) -> int:
        beacons_cannot_be_in_x = set()
        beacons_in_target_y = set()

        for sx, sy, bx, by in self.observations:
            extent = abs(sx - bx) + abs(sy - by) - abs(sy - self.target_y)
            beacons_cannot_be_in_x.update(set(range(sx - extent, sx + extent + 1)))

            if by == self.target_y:
                beacons_in_target_y.add(bx)

        return len(beacons_cannot_be_in_x - beacons_in_target_y)

    def z3_abs(self, val: int):
        return If(val >= 0, val, -val)

    def part2(self) -> int:
        solver = Solver()

        x, y = Int('x'), Int('y')

        solver.add(x >= 0)
        solver.add(x <= self.max_coord)
        solver.add(y >= 0)
        solver.add(y <= self.max_coord)

        for sx, sy, bx, by in self.observations:
            manhattan_distance = abs(sx - bx) + abs(sy - by)
            solver.add(self.z3_abs(sx - x) + self.z3_abs(sy - y) > manhattan_distance)

        assert solver.check()

        model = solver.model()

        return model[x].as_long() * 4000000 + model[y].as_long()

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
                    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
                    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
                    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
                    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
                    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
                    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
                    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
                    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
                    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
                    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
                    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
                    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
                    'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
                ],
                'part1': 26,
                'part2': 56000011,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            self.target_y = 10
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            self.max_coord = 20
            assert self.part2() == test['part2']

        self.common(input_data)
        self.target_y = 2000000
        assert self.part1() == 4879972
        self.common(input_data)
        self.max_coord = 4000000
        assert self.part2() == 12525726647448

        return len(tests) + 1
