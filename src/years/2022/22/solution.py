

from re import findall
from typing import Optional, Union

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

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)


TuplePositionInt = tuple[Position, int]


class Puzzle22(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        input_data = [line.rstrip() for line in input_data]
        self.directions = {0: Position(0, 1), 1: Position(1, 0), 2: Position(0, -1), 3: Position(-1, 0)}
        self.rotations = {'L': -1, 'R': 1}
        self.diagonals = {0: Position(1, 1), 1: Position(1, -1), 2: Position(-1, -1), 3: Position(-1, 1)}

        self.instructions = findall(r'(\d+|L|R)', input_data[-1])
        self.start = Position(-1, -1)
        self.max_rows = len(input_data[:-2])
        self.max_cols = 0
        board = []

        for line in input_data[:-2]:
            board.append(list(line))
            self.max_cols = max(self.max_cols, len(line))

        self.board = [
            parsed_line + [' '] * (self.max_cols - len(parsed_line))
            for parsed_line in board
        ]

        self.start = Position(0, self.board[0].index('.'))

    def within_bounds(self, position: Position) -> bool:
        return not (
            position.x < 0
            or position.y < 0
            or position.x >= self.max_rows
            or position.y >= self.max_cols
            or self.board[position.x][position.y] == ' '
        )

    def execute_step(self, position: Position, direction: int) -> TuplePositionInt:
        new_position = position + self.directions[direction]
        new_direction = direction

        if not self.within_bounds(new_position):
            key_in = (position, direction)

            new_position = self.adjacency_dict[key_in][0]
            new_direction = self.adjacency_dict[key_in][1]

        if self.board[new_position.x][new_position.y] == '#':
            return position, direction
        else:
            return new_position, new_direction

    def execute_instruction(self, position: Position, direction: int, instruction: Union[str, int]) -> TuplePositionInt:
        new_direction = direction
        if instruction == 'L' or instruction == 'R':
            new_direction += self.rotations[str(instruction)]
            new_direction %= 4
        else:
            for _ in range(int(instruction)):
                position, new_direction = self.execute_step(position, new_direction)

        return position, new_direction

    def perimeter_step(self, position: Position, direction: int):
        new_position = position + self.directions[direction]

        if not self.within_bounds(new_position):
            direction_l = (direction - 1) % 4
            new_position_l = position + self.directions[direction_l]

            direction_r = (direction + 1) % 4
            new_position_r = position + self.directions[direction_r]

            if self.within_bounds(new_position_l):
                return position, direction_l

            if self.within_bounds(new_position_r):
                return position, direction_r

        return new_position, direction

    def check_if_inner_corner(self, position: Position) -> tuple[bool, Optional[list[list[int]]]]:
        if not self.within_bounds(position):
            return False, None

        direction_pair_list = []

        for idx in range(4):
            if (
                self.within_bounds(position + self.directions[idx])
                and self.within_bounds(position + self.directions[(idx + 1) % 4])
                and not self.within_bounds(position + self.diagonals[idx])
            ):
                direction_pair_list.append([idx, (idx + 1) % 4])

        if len(direction_pair_list) > 0:
            return True, direction_pair_list
        else:
            return False, None

    def zip_up_edges_from_corner(self, position: Position, direction_pair: list[int]) -> None:
        direction0 = direction_pair[0]
        direction1 = direction_pair[1]

        direction0_prev = direction0
        direction1_prev = direction1

        position0 = position + self.directions[direction0]
        position1 = position + self.directions[direction1]

        while direction0 == direction0_prev or direction1_prev == direction1:
            direction0_prev = direction0
            direction1_prev = direction1

            normal_direction_outer0 = (direction0 + 1) % 4
            if self.within_bounds(position0 + self.directions[normal_direction_outer0]):
                normal_direction_outer0 = (direction0 - 1) % 4

            normal_direction_outer1 = (direction1 + 1) % 4
            if self.within_bounds(position1 + self.directions[normal_direction_outer1]):
                normal_direction_outer1 = (direction1 - 1) % 4

            normal_direction_inner0 = (normal_direction_outer0 + 2) % 4
            normal_direction_inner1 = (normal_direction_outer1 + 2) % 4

            self.dict_out[(position0, normal_direction_outer0)] = (position1, normal_direction_inner1)
            self.dict_out[(position1, normal_direction_outer1)] = (position0, normal_direction_inner0)

            position0, direction0 = self.perimeter_step(position0, direction0)
            position1, direction1 = self.perimeter_step(position1, direction1)

            bool0, _ = self.check_if_inner_corner(position0)
            bool1, _ = self.check_if_inner_corner(position1)

            if bool0 or bool1:
                break

    def generate_off_grid_adjacency_cube(self) -> dict[TuplePositionInt, TuplePositionInt]:
        self.dict_out: dict[TuplePositionInt, TuplePositionInt] = {}

        for row in range(self.max_rows):
            for col in range(self.max_cols):
                position = Position(row, col)

                corner_bool, direction_pair_list = self.check_if_inner_corner(position)
                if corner_bool:
                    if direction_pair_list is not None:
                        for direction_pair in direction_pair_list:
                            self.zip_up_edges_from_corner(position, direction_pair)

        return self.dict_out

    def generate_off_grid_adjacency_wrap(self) -> dict[TuplePositionInt, TuplePositionInt]:
        dict_out = {}

        for idx in range(self.max_rows):
            left = 0
            while self.board[idx][left] == ' ':
                left += 1

            right = self.max_cols - 1
            while self.board[idx][right] == ' ':
                right -= 1

            dict_out[(Position(idx, left), 2)] = (Position(idx, right), 2)
            dict_out[(Position(idx, right), 0)] = (Position(idx, left), 0)

        for idx in range(self.max_cols):
            top = 0
            while self.board[top][idx] == ' ':
                top += 1

            bottom = self.max_rows - 1
            while self.board[bottom][idx] == ' ':
                bottom -= 1

            dict_out[(Position(top, idx), 3)] = (Position(bottom, idx), 3)
            dict_out[(Position(bottom, idx), 1)] = (Position(top, idx), 1)

        return dict_out

    def follow_instructions(self):
        direction = 0
        position = self.start

        for instruction in self.instructions:
            position, direction = self.execute_instruction(position, direction, instruction)

        return 1000 * (position.x + 1) + 4 * (position.y + 1) + direction

    def part1(self) -> int:
        self.adjacency_dict = self.generate_off_grid_adjacency_wrap()

        return self.follow_instructions()

    def part2(self) -> int:
        self.adjacency_dict = self.generate_off_grid_adjacency_cube()

        return self.follow_instructions()

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '        ...#',
                    '        .#..',
                    '        #...',
                    '        ....',
                    '...#.......#',
                    '........#...',
                    '..#....#....',
                    '..........#.',
                    '        ...#....',
                    '        .....#..',
                    '        .#......',
                    '        ......#.',
                    '',
                    '10R5L5R10L4R5L5',
                ],
                'part1': 6032,
                'part2': 5031,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 47462
        self.common(input_data)
        assert self.part2() == 137045

        return len(tests) + 1
