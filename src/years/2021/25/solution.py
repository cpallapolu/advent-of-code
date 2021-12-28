
from collections import defaultdict
from itertools import count

from aocpuzzle import AoCPuzzle

CoordType = tuple[int, int]

EMPTY = '.'
EAST = '>'
SOUTH = 'v'


class Puzzle25(AoCPuzzle):
    def print_grid(self) -> None:
        for row in range(self.rows + 1):
            line = (self.cucumbers[(row, col)] for col in range(self.cols + 1))
            print(''.join(line))

    def common(self, input_data: list[str]) -> None:
        self.cucumbers: dict[CoordType, str] = defaultdict(lambda: EMPTY)
        self.rows, self.cols = 0, 0

        for row, line in enumerate(input_data):
            for col, val in enumerate(line):
                self.cucumbers[(row, col)] = val
                self.rows = max(self.rows, row + 1)
                self.cols = max(self.cols, col + 1)

    def move(self) -> int:
        for step in count(1):
            moves = []

            for row in range(self.rows):
                for col in range(self.cols):
                    new_forward_row = (row + 1) % self.rows

                    new_forward_col = (col + 1) % self.cols
                    new_backward_col = (col - 1) % self.cols

                    east_can_move = (
                        self.cucumbers[(row, col)] == EAST
                        and self.cucumbers[(row, new_forward_col)] == EMPTY
                    )
                    south_can_move = (
                        self.cucumbers[(row, col)] == SOUTH
                        and self.cucumbers[(new_forward_row, col)] == EMPTY
                        and self.cucumbers[(new_forward_row, new_backward_col)] != EAST
                    )
                    south_can_move_after_east_move = (
                        self.cucumbers[(row, col)] == SOUTH
                        and self.cucumbers[(new_forward_row, col)] == EAST
                        and self.cucumbers[(new_forward_row, new_forward_col)] == EMPTY
                    )

                    if east_can_move or south_can_move_after_east_move or south_can_move:
                        moves.append((self.cucumbers[(row, col)], row, col))

            if len(moves) == 0:
                break

            for char, row, col in sorted(moves):
                self.cucumbers[(row, col)] = EMPTY

                if char == EAST:
                    self.cucumbers[(row, (col + 1) % self.cols)] = char
                else:
                    self.cucumbers[((row + 1) % self.rows, col)] = char

        return step

    def part1(self) -> int:
        return self.move()

    def part2(self) -> str:
        return 'Remotely Start The Sleigh'

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'v...>>.vv>',
                    '.vv>>.vv..',
                    '>>.>v>...v',
                    '>>v>>.>.v.',
                    'v>v.vv.v..',
                    '>.>>..v...',
                    '.vv..>.>v.',
                    'v.v..>>v.v',
                    '....v..v.>',
                ],
                'part1': 58,
                'part2': 'Remotely Start The Sleigh',
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 516
        self.common(input_data)
        assert self.part2() == 'Remotely Start The Sleigh'

        return len(tests) + 1
