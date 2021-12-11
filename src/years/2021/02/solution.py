

from aocpuzzle import AoCPuzzle


class Submarine:
    def __init__(self) -> None:
        self.horizontal_position = 0
        self.depth = 0
        self.aim = 0
        self.FORWARD = 'forward'
        self.DOWN = 'down'
        self.UP = 'up'

    def move(self, direction: str, units: int, corrected=False) -> None:
        if direction == self.FORWARD:
            self.move_forward(units, corrected)

        if direction == self.DOWN:
            self.move_down(units, corrected)

        if direction == self.UP:
            self.move_up(units, corrected)

    def move_forward(self, units: int, corrected=False) -> None:
        if corrected is False:
            self.horizontal_position += units
        else:
            self.horizontal_position += units
            self.depth += (self.aim * units)

    def move_down(self, units: int, corrected=False) -> None:
        if corrected is False:
            self.depth += units
        else:
            self.aim += units

    def move_up(self, units: int, corrected=False) -> None:
        if corrected is False:
            self.depth -= units
        else:
            self.aim -= units


class Puzzle02(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.movements = []

        for movement in input_data:
            [direction, unit] = movement.split(' ')
            self.movements.append((direction, int(unit)))

        self.submarine = Submarine()

    def part1(self) -> int:
        for (direction, units) in self.movements:
            self.submarine.move(direction, units)

        return self.submarine.horizontal_position * self.submarine.depth

    def part2(self) -> int:
        for (direction, units) in self.movements:
            self.submarine.move(direction, units, True)

        return self.submarine.horizontal_position * self.submarine.depth

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'forward 5',
                    'down 5',
                    'forward 8',
                    'up 3',
                    'down 8',
                    'forward 2',
                ],
                'part1': 150,
                'part2': 900,
            },
        ]

        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 2147104
        self.common(input_data)
        assert self.part2() == 2044620088

        return len(tests) + 1
