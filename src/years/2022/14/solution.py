

from collections import defaultdict

from aocpuzzle import AoCPuzzle

ROCK = '#'
AIR = '.'
SAND_REST = 'o'


class Puzzle14(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.cave: dict[tuple[int, int], str] = defaultdict(lambda: AIR)
        self.sand_source_x, self.sand_source_y = 500, 0
        self.max_y = 0

        for line in input_data:
            parse_line = [list(map(int, p.split(','))) for p in line.strip().split(' -> ')]

            for (x1, y1), (x2, y2) in zip(parse_line[:-1], parse_line[1:]):
                start_x, end_x = sorted([x1, x2])
                start_y, end_y = sorted([y1, y2])

                for x in range(start_x, end_x + 1):
                    for y in range(start_y, end_y + 1):
                        self.cave[(x, y)] = ROCK

                self.max_y = max(self.max_y, end_y)

    def simulate_sand_fall(self, has_finite_bottom=False) -> int:
        moves = [(0, 1), (-1, 1), (1, 1)]

        curr_x, curr_y = self.sand_source_x, self.sand_source_y

        while (curr_x, curr_y) not in self.cave:
            if curr_y > self.max_y:
                return False

            can_move = False

            for (move_x, move_y) in moves:
                new_x, new_y = curr_x + move_x, curr_y + move_y

                if has_finite_bottom and new_y == self.max_y:
                    self.cave[(new_x, new_y)] = ROCK
                    break

                if (new_x, new_y) not in self.cave:
                    curr_x, curr_y = new_x, new_y
                    can_move = True
                    break

            if can_move:
                continue

            self.cave[(curr_x, curr_y)] = SAND_REST

        return True

    def part1(self) -> int:
        total_sand = 0

        while self.simulate_sand_fall():
            total_sand += 1

        return total_sand

    def part2(self) -> int:
        self.max_y += 2

        total_sand = 0

        while (self.sand_source_x, self.sand_source_y) not in self.cave:
            self.simulate_sand_fall(True)
            total_sand += 1

        return total_sand

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '498, 4 -> 498, 6 -> 496, 6',
                    '503, 4 -> 502, 4 -> 502, 9 -> 494, 9',
                ],
                'part1': 24,
                'part2': 93,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 858
        self.common(input_data)
        assert self.part2() == 26845

        return len(tests) + 1
