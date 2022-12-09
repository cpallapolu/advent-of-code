

from aocpuzzle import AoCPuzzle


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Puzzle09(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.moves = [(move[0], int(move.split().pop(-1))) for move in input_data]

        self.directions = {
            'U': Position(0, 1),
            'D': Position(0, -1),
            'L': Position(-1, 0),
            'R': Position(1, 0),
        }

    def move_sign(self, x: int, y: int) -> int:
        if x > y:
            return 1
        elif x < y:
            return -1
        else:
            return 0

    def move_tail(self, head: Position, tail: Position) -> Position:
        update_tail = False

        # Check if we need to move diagonally
        if abs(head.x - tail.x) + abs(head.y - tail.y) > 2:
            update_tail = True

        # Check if we need to move horizontally/vertically.
        if (head.x == tail.x or head.y == tail.y) and (abs(head.x - tail.x) + abs(head.y - tail.y) > 1):
            update_tail = True

        tail += (
            Position(self.move_sign(head.x, tail.x), self.move_sign(head.y, tail.y))
            if update_tail
            else Position(0, 0)
        )

        return tail

    def simulate_moves(self, knots_num: int) -> int:
        knots = [Position(0, 0) for _ in range(knots_num)]

        tail_visited_pos: set[Position] = set()

        for (direction, steps) in self.moves:
            for _ in range(steps):
                knots[0] += self.directions[direction]

                for knot in range(1, knots_num):
                    knots[knot] = self.move_tail(knots[knot - 1], knots[knot])

                tail_visited_pos.add(knots[-1])

        return len(tail_visited_pos)

    def part1(self) -> int:
        return self.simulate_moves(2)

    def part2(self) -> int:
        return self.simulate_moves(10)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'R 4',
                    'U 4',
                    'L 3',
                    'D 1',
                    'R 4',
                    'D 1',
                    'L 5',
                    'R 2',
                ],
                'part1': 13,
                'part2': 1,
            },
            {
                'input_data': [
                    'R 5'
                    'U 8'
                    'L 8'
                    'D 3'
                    'R 17'
                    'D 10'
                    'L 25'
                    'U 20',
                ],
                'part1': 20,
                'part2': 12,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 6256
        self.common(input_data)
        assert self.part2() == 2665

        return len(tests) + 1
