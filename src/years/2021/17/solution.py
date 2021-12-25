

from re import findall

from aocpuzzle import AoCPuzzle


class Puzzle17(AoCPuzzle):
    def get_target_area_coords(self, x1: int, x2: int, y1: int, y2: int) -> set[tuple[int, int]]:
        return set(
            (x, y)
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
        )

    def shoot(self, x_vel, y_vel) -> tuple[bool, int]:
        start_x, start_y = 0, 0
        max_y = 0

        while True:
            start_x += x_vel
            start_y += y_vel

            max_y = max(start_y, max_y)

            x_vel += 0 if x_vel == 0 else -1 if x_vel > 0 else 1
            y_vel -= 1

            if (start_x, start_y) in self.target_area_coords:
                return True, max_y

            if start_y < self.target_y_min or start_x > self.target_x_max:
                return False, 0

    def common(self, input_data: str) -> None:
        target_area = findall(r'x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', input_data)

        self.target_x_min, self.target_x_max, self.target_y_min, self.target_y_max = (
            int(num) for num in target_area[0]
        )

        self.target_area_coords = self.get_target_area_coords(
            self.target_x_min, self.target_x_max, self.target_y_min, self.target_y_max,
        )
        self.hits: int = 0
        self.max_y_positions: int = 0

    def try_hits(self) -> None:
        for x_vel in range(0, self.target_x_max + 1):
            for y_vel in range(abs(self.target_y_min), self.target_y_min - 1, - 1):
                in_target, max_y = self.shoot(x_vel, y_vel)

                if in_target is True:
                    self.hits += 1
                    self.max_y_positions = max(self.max_y_positions, max_y)

    def part1(self) -> int:
        self.try_hits()

        return self.max_y_positions

    def part2(self) -> int:
        self.try_hits()

        return self.hits

    def test_cases(self, input_data: str) -> int:
        tests: list[dict] = [
            {
                'input_data': 'target area: x=20..30, y=-10..-5',
                'part1': 45,
                'part2': 112,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 3655
        self.common(input_data)
        assert self.part2() == 1447

        return len(tests) + 1
