
from collections import defaultdict

from aocpuzzle import AoCPuzzle


class Puzzle05(AoCPuzzle):
    def get_coordinate_range(self, a: int, b: int, c: int, d: int) -> list[int]:
        if a == b:
            return [a] * (abs(c - d) + 1)

        return list(range(a, b - 1, -1)) if a > b else list(range(a, b + 1))

    def is_horizontal_or_vertical(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        return x1 == x2 or y1 == y2

    def points(self, x1: int, y1: int, x2: int, y2: int):
        return zip(
            self.get_coordinate_range(x1, x2, y1, y2),
            self.get_coordinate_range(y1, y2, x1, x2),
        )

    def common(self, input_data: list[str]) -> None:
        self.lines = []

        for entry in input_data:
            start, end = entry.split(' -> ')
            x1, y1 = tuple(map(int, start.split(',')))
            x2, y2 = tuple(map(int, end.split(',')))

            self.lines.append([x1, y1, x2, y2])

    def part1(self) -> int:
        horizontal_vertical_overlaps: dict[int, int] = defaultdict(int)

        for line in self.lines:
            for point in self.points(*line):
                horizontal_vertical_overlaps[point] += self.is_horizontal_or_vertical(*line)

        return sum([
            overlap > 1
            for overlap in horizontal_vertical_overlaps.values()
        ])

    def part2(self) -> int:
        overlaps: dict[int, int] = defaultdict(int)

        for line in self.lines:
            for point in self.points(*line):
                overlaps[point] += 1

        return sum([
            overlap > 1
            for overlap in overlaps.values()
        ])

    def test_cases(self, input_data: list[str]) -> int:
        tests = [
            [
                '0,9 -> 5,9',
                '8,0 -> 0,8',
                '9,4 -> 3,4',
                '2,2 -> 2,1',
                '7,0 -> 7,4',
                '6,4 -> 2,0',
                '0,9 -> 2,9',
                '3,4 -> 1,4',
                '0,0 -> 8,8',
                '5,5 -> 8,2',
            ],
        ]
        for test in tests:
            self.common(test)
            assert self.part1() == 5
            self.common(test)
            assert self.part2() == 12

        self.common(input_data)
        assert self.part1() == 5294
        self.common(input_data)
        assert self.part2() == 21698

        return len(tests) + 1
