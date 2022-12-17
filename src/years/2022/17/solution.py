

from enum import IntEnum

from aocpuzzle import AoCPuzzle


class Shapes(IntEnum):
    HORIZONTAL_LINE = 0
    PLUS = 1
    RIGHT_ANGLE = 2
    VERTICAL_BAR = 3
    SQUARE = 4


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'(x, y): ({self.x}, {self.y})'

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


ROCKS = [
    [Position(2, 0), Position(3, 0), Position(4, 0), Position(5, 0)],  # Horizontal Line
    [Position(3, 0), Position(2, 1), Position(3, 1), Position(4, 1), Position(3, 2)],  # Plus
    [Position(2, 0), Position(3, 0), Position(4, 0), Position(4, 1), Position(4, 2)],  # Angle
    [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],  # Vertical Bar
    [Position(2, 0), Position(2, 1), Position(3, 0), Position(3, 1)],  # Square
]


class Rock:
    def __init__(self, shape: int, position: Position) -> None:
        self.position = position

        self.rock: list[Position] = ROCKS[shape]

    def positions(self) -> set[Position]:
        return {
            Position(rock_position.x + self.position.x, rock_position.y + self.position.y)
            for rock_position in self.rock
        }

    def move(self, delta: Position) -> None:
        self.position.x += delta.x
        self.position.y += delta.y


class Chamber:
    def __init__(self, width: int, winds: str) -> None:
        self.width = width
        self.winds = winds

        self.filled: set[Position] = set()
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
                Position(p.x, p.y - height) for p in self.filled if p.y >= height
            }
            self.base_height += height
            self.top -= height
            self.columns = [c - height for c in self.columns]

        self.height = self.base_height + self.top + 1

    def simulate_fall(self) -> None:
        rock = Rock(self.rock_idx, Position(0, self.top + 4))
        positions = rock.positions()
        move = Position(0, 0)

        while True:
            wind_dir = -1 if self.winds[self.wind_idx] == '<' else 1
            self.wind_idx = (self.wind_idx + 1) % len(self.winds)

            next_horizontal_positions = {Position(p.x + wind_dir, p.y) for p in positions}
            if all(p.x >= 0 and p.x < self.width and p not in self.filled for p in next_horizontal_positions):
                move.x += wind_dir
                positions = next_horizontal_positions

            next_vertical_positions = {Position(p.x, p.y - 1) for p in positions}
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
        self.tower_width = 7
        self.jet_stream = input_data
        self.jump_height = 0

        self.human_size = 2022
        self.elephant_size = 1_000_000_000_000
        self.states: dict[str, tuple[int, int]] = {}

    def save_state(self, chamber: Chamber) -> None:
        if self.curr_cycle < 2022:
            return

        state_key = '|'.join(map(str, [chamber.rock_idx, chamber.wind_idx, *map(str, chamber.columns)]))

        if state_key in self.states:
            cycles, height = self.states[state_key]
            loops = ((self.elephant_size - cycles) // (self.curr_cycle - cycles)) - 1
            self.jump_height = loops * (chamber.height - height)

            self.curr_cycle += loops * (self.curr_cycle - cycles)

            self.states = {}

        self.states[state_key] = (self.curr_cycle, chamber.height)

    def solve(self, cycles: int) -> int:
        chamber = Chamber(self.tower_width, self.jet_stream)
        self.curr_cycle = 0

        while self.curr_cycle < cycles:
            chamber.simulate_fall()
            self.curr_cycle += 1

            self.save_state(chamber)

        return self.jump_height + chamber.height

    def part1(self) -> int:
        return self.solve(self.human_size)

    def part2(self) -> int:
        return self.solve(self.elephant_size)

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
