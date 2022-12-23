

from collections import defaultdict
from math import prod

from aocpuzzle import AoCPuzzle

EMPTY = '.'
OCCUPIED = '#'


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


class Puzzle23(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.elves_positions: set[Position] = {
            Position(row_idx, col_idx)
            for row_idx, row in enumerate(input_data)
            for col_idx, col in enumerate(row)
            if col == OCCUPIED
        }

        self.moving_sequences = [
            [Position(-1, 0), Position(-1, 1), Position(-1, -1)],  # North
            [Position(1, 0), Position(1, 1), Position(1, -1)],  # South
            [Position(0, -1), Position(-1, -1), Position(1, -1)],  # West
            [Position(0, 1), Position(-1, 1), Position(1, 1)],  # East
        ]

    def print_grid(self) -> None:
        print('=============================================')
        min_x = min(position.x for position in self.elves_positions)
        max_x = max(position.x for position in self.elves_positions)
        min_y = min(position.y for position in self.elves_positions)
        max_y = max(position.y for position in self.elves_positions)

        x_range = max_x - min_x + 1
        y_range = max_y - min_y + 1
        print(x_range, y_range)
        for x in range(min_x, max_x + 1):
            line = ''
            for y in range(min_y, max_y + 1):
                line += OCCUPIED if Position(x, y) in self.elves_positions else EMPTY
            print(line)

    def move_elves(self) -> int:
        elves_can_move_to: dict[Position, list[Position]] = defaultdict(list)

        for elf_position in self.elves_positions:
            has_any_neighbors = any([
                elf_position + Position(x, y) in self.elves_positions
                for x in range(-1, 2, 1)
                for y in range(-1, 2, 1)
                if (x, y) != (0, 0)
            ])

            if not has_any_neighbors:
                continue

            for moving_sequence in self.moving_sequences:
                any_position_occupied = any([
                    elf_position + sequence_position in self.elves_positions
                    for sequence_position in moving_sequence
                ])

                if not any_position_occupied:
                    elves_can_move_to[elf_position + moving_sequence[0]].append(elf_position)

                    break

        self.moving_sequences = self.moving_sequences[1:] + self.moving_sequences[:1]

        moves = 0
        for elf_can_move_to, total_elves in elves_can_move_to.items():
            if len(total_elves) > 1:
                continue

            self.elves_positions.add(elf_can_move_to)
            self.elves_positions.remove(total_elves[0])
            moves += 1

        return moves

    def get_rectangle_dimensions(self) -> tuple[int, int]:

        min_x = min(position.x for position in self.elves_positions)
        max_x = max(position.x for position in self.elves_positions)
        min_y = min(position.y for position in self.elves_positions)
        max_y = max(position.y for position in self.elves_positions)

        return (max_x - min_x + 1), (max_y - min_y + 1)

    def part1(self) -> int:
        for _ in range(10):
            self.move_elves()

        return prod(self.get_rectangle_dimensions()) - len(self.elves_positions)

    def part2(self) -> int:
        rounds_with_movement = 1

        while self.move_elves() > 0:
            rounds_with_movement += 1

        return rounds_with_movement

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '.....',
                    '..##.',
                    '..#..',
                    '.....',
                    '..##.',
                    '.....',
                ],
                'part1': 25,
                'part2': 4,
            },
            {
                'input_data': [
                    '....#..',
                    '..###.#',
                    '#...#.#',
                    '.#...##',
                    '#.###..',
                    '##.#.##',
                    '.#..#..',
                ],
                'part1': 110,
                'part2': 20,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 4249
        self.common(input_data)
        assert self.part2() == 980

        return len(tests) + 1
