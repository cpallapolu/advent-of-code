

from enum import IntEnum

from aocpuzzle import AoCPuzzle
from years.utils.common import remove_newline
from years.utils.geo import Position2D


class Shapes(IntEnum):
    HORIZONTAL_LINE = 0
    PLUS = 1
    RIGHT_ANGLE = 2
    VERTICAL_BAR = 3
    SQUARE = 4


ROCKS = [
    [Position2D(2, 0), Position2D(3, 0), Position2D(4, 0), Position2D(5, 0)],  # Horizontal Line
    [Position2D(3, 0), Position2D(2, 1), Position2D(3, 1), Position2D(4, 1), Position2D(3, 2)],  # Plus
    [Position2D(2, 0), Position2D(3, 0), Position2D(4, 0), Position2D(4, 1), Position2D(4, 2)],  # Angle
    [Position2D(2, 0), Position2D(2, 1), Position2D(2, 2), Position2D(2, 3)],  # Vertical Bar
    [Position2D(2, 0), Position2D(2, 1), Position2D(3, 0), Position2D(3, 1)],  # Square
]


class Rock:
    def __init__(self, shape: int, position: Position2D) -> None:
        self.position = position

        self.rock: list[Position2D] = ROCKS[shape]

    def positions(self) -> set[Position2D]:
        return {
            Position2D(rock_position.x + self.position.x, rock_position.y + self.position.y)
            for rock_position in self.rock
        }

    def move(self, delta: Position2D) -> None:
        self.position.x += delta.x
        self.position.y += delta.y


class Chamber:
    def __init__(self, width: int, winds: str) -> None:
        self.width = width
        self.winds = winds

        self.filled: set[Position2D] = set()
        self.columns = [-1 for _ in range(width)]
        self.base_height = 0
        self.top = -1
        self.rock_idx = int(Shapes.HORIZONTAL_LINE)
        self.wind_idx = 0

    def __str__(self) -> str:
        return ''.join(
            '|' + ''.join('#' if x + y * 1j in self.filled else '.' for x in range(self.width)) + '|\n'
            for y in range(self.top, -1, -1)
        ) + '+' + '-' * self.width + '+'

    def add_rock(self, rock: Rock) -> None:
        positions = rock.positions()
        self.filled = self.filled.union(positions)

        for col, height in ((p.x, p.y) for p in positions):
            self.columns[col] = max(self.columns[col], height)
            self.top = max(self.top, height)

    def fill_chamber(self) -> None:
        height = min(self.columns)

        if height > 1:
            self.filled = {
                Position2D(p.x, p.y - height) for p in self.filled if p.y >= height
            }
            self.base_height += height
            self.top -= height
            self.columns = [c - height for c in self.columns]

    def height(self) -> int:
        return self.base_height + self.top + 1

    def simulate_fall(self) -> None:
        rock = Rock(self.rock_idx, Position2D(0, self.top + 4))
        positions = rock.positions()
        move = Position2D(0, 0)

        while True:
            wind_dir = -1 if self.winds[self.wind_idx] == '<' else 1
            self.wind_idx = (self.wind_idx + 1) % len(self.winds)

            next_horizontal_positions = {Position2D(p.x + wind_dir, p.y) for p in positions}
            if all(p.x >= 0 and p.x < self.width and p not in self.filled for p in next_horizontal_positions):
                move.x += wind_dir
                positions = next_horizontal_positions

            next_vertical_positions = {Position2D(p.x, p.y - 1) for p in positions}
            if any(p.y < 0 or p in self.filled for p in next_vertical_positions):
                break

            move.y += -1
            positions = next_vertical_positions

        rock.move(move)
        self.add_rock(rock)
        self.fill_chamber()

        self.rock_idx = (self.rock_idx + 1) % len(Shapes)


class Puzzle17(AoCPuzzle):
    def common(self, input_data: str) -> None:
        input_data = remove_newline(input_data)

        self.tower_width = 7
        self.jet_stream = input_data

    def part1(self) -> int:
        cavern = Chamber(self.tower_width, self.jet_stream)
        attempt = 0

        while attempt < 2022:
            cavern.simulate_fall()
            attempt += 1

        return cavern.height()

    def part2(self) -> int:
        cavern = Chamber(self.tower_width, self.jet_stream)
        attempt = 0
        jump_height = 0
        elephant_size = 1_000_000_000_000
        state: dict[str, tuple[int, int]] = {}
        while attempt < elephant_size:
            cavern.simulate_fall()
            attempt += 1

            state_key = '|'.join(map(str, (cavern.rock_idx, cavern.wind_idx, '|'.join(map(str, cavern.columns)))))

            if state_key in state:
                attempts, height = state[state_key]
                loops = ((elephant_size - attempts) // (attempt - attempts)) - 1
                jump_height = loops * (cavern.height() - height)
                attempt += loops * (attempt - attempts)
                state = {}

            state[state_key] = (attempt, cavern.height())

        return jump_height + cavern.height()

    def test_cases(self, input_data: str) -> int:

        tests: list[dict] = [
            {
                'input_data': '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>',
                'part1': 3068,
                'part2': 1514285714288,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 3114
        self.common(input_data)
        assert self.part2() == 1540804597682

        return len(tests) + 1
