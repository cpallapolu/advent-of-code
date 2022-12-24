

from aocpuzzle import AoCPuzzle


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


UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

DIRECTIONS = {
    UP: Position(-1, 0),
    DOWN: Position(1, 0),
    LEFT: Position(0, -1),
    RIGHT: Position(0, 1),
}


class Blizzard:
    def __init__(self, direction_symbol: str, position: Position) -> None:
        self.direction_symbol = direction_symbol
        self.position = position

    def __str__(self) -> str:
        return f'Direction: {self.direction_symbol}, position: {self.position}'


class Puzzle24(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        input_data = [line.strip() for line in input_data]

        self.blizzards = set()
        self.walls = set()
        self.rows, self.cols = 0, 0

        for row_idx, row in enumerate(input_data):
            for col_idx, col in enumerate(row):
                position = Position(row_idx, col_idx)
                self.rows = max(self.rows, row_idx + 1)
                self.cols = max(self.cols, col_idx + 1)

                if col == '#':
                    self.walls.add(position)

                if col not in '.#':
                    self.blizzards.add(Blizzard(col, position))

        self.start = Position(0, 1)
        self.target = Position(self.rows - 1, self.cols - 2)

        self.walls.add(Position(self.start.x - 1, self.start.y))
        self.walls.add(Position(self.target.x + 1, self.target.y))

    def within_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.rows and 0 <= position.y < self.cols and position not in self.walls

    def move(self, blizzard: Blizzard) -> None:
        new_pos = blizzard.position + DIRECTIONS[blizzard.direction_symbol]

        if self.within_bounds(new_pos):
            blizzard.position = new_pos
        elif blizzard.direction_symbol == UP:
            blizzard.position.x = self.rows - 2
        elif blizzard.direction_symbol == DOWN:
            blizzard.position.x = 1
        elif blizzard.direction_symbol == LEFT:
            blizzard.position.y = self.cols - 2
        elif blizzard.direction_symbol == RIGHT:
            blizzard.position.y = 1

    def move_to_target(self, start: Position, target: Position) -> None:
        states = set([start])

        while target not in states:
            self.step += 1

            cannot_move_to = set(self.walls)

            for blizzard in self.blizzards:
                self.move(blizzard)
                cannot_move_to.add(blizzard.position)

            new_states = set()

            for state in states:
                for direction_delta in DIRECTIONS.values():
                    new_pos = state + direction_delta

                    if new_pos not in cannot_move_to:
                        new_states.add(new_pos)

                if state not in cannot_move_to:
                    new_states.add(state)

            states = new_states

    def part1(self) -> int:
        self.step = 0
        self.steps_arr = []

        self.move_to_target(self.start, self.target)
        self.steps_arr.append(self.step)

        return self.step

    def part2(self) -> int:
        self.step = 0
        self.steps_arr = []

        self.move_to_target(self.start, self.target)
        self.steps_arr.append(self.step)

        self.move_to_target(self.target, self.start)
        self.steps_arr.append(self.step - sum(self.steps_arr))

        self.move_to_target(self.start, self.target)
        self.steps_arr.append(self.step - sum(self.steps_arr))

        return self.step

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '#.#####',
                    '#.....#',
                    '#>....#',
                    '#.....#',
                    '#...v.#',
                    '#.....#',
                    '#####.#',
                ],
                'part1': 10,
                'part2': 30,
                'part1_steps_arr': [10],
                'part2_steps_arr': [10, 10, 10],
            },
            {
                'input_data': [
                    '#.######',
                    '#>>.<^<#',
                    '#.<..<<#',
                    '#>v.><>#',
                    '#<^v^^>#',
                    '######.#',
                ],
                'part1': 18,
                'part2': 54,
                'part1_steps_arr': [18],
                'part2_steps_arr': [18, 23, 13],
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            assert self.steps_arr == test['part1_steps_arr']

            self.common(test['input_data'])
            assert self.part2() == test['part2']
            assert self.steps_arr == test['part2_steps_arr']

        self.common(input_data)
        assert self.part1() == 334
        assert self.steps_arr == [334]
        self.common(input_data)
        assert self.part2() == 934
        assert self.steps_arr == [334, 309, 291]

        return len(tests) + 1
