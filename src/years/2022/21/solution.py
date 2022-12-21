

from typing import Optional

from z3 import Int, Solver

from aocpuzzle import AoCPuzzle

OPS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b if isinstance(a, int) and isinstance(b, int) else a / b,
    '=': lambda a, b: a == b,
}


class MonkeyOp:
    def __init__(self, line: str) -> None:
        self.name = ''
        self.shouted_number: Optional[int] = None
        self.left = ''
        self.op = ''
        self.right = ''

        self.parse_line(line)

    def parse_line(self, line: str):
        name, rest = line.split(': ')
        self.name = name

        if rest.isdigit():
            self.shouted_number = int(rest)
        else:
            left, op, right = rest.split(' ')
            self.left = left
            self.op = op
            self.right = right

    def __str__(self) -> str:
        out_lines = [
            f'Monkey: {self.name}',
            f'shouted_number: {self.shouted_number}',
            f'left: {self.left}',
            f'op: {self.op}',
            f'right: {self.right}',
        ]
        return ', '.join(out_lines)


class Puzzle21(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.monkeys = {}

        for line in input_data:
            monkey_op = MonkeyOp(line)
            self.monkeys[monkey_op.name] = monkey_op

    def evaluate(self, is_part2: bool) -> bool:
        monkeys_queue = list(
            monkey
            for monkey in self.monkeys.values()
            if monkey.shouted_number is None
        )

        while len(monkeys_queue) > 0:
            curr_monkey = monkeys_queue.pop(0)

            left_monkey_number = self.monkeys[curr_monkey.left].shouted_number
            right_monkey_number = self.monkeys[curr_monkey.right].shouted_number

            if left_monkey_number is None or right_monkey_number is None:
                monkeys_queue.append(curr_monkey)
                continue

            if is_part2 and curr_monkey.name == 'root':
                self.z3_solver.add(left_monkey_number == right_monkey_number)

                return True
            evaluated_number = OPS[curr_monkey.op](left_monkey_number, right_monkey_number)
            self.monkeys[curr_monkey.name].shouted_number = evaluated_number

        return False

    def part1(self) -> int:
        self.z3_solver = Solver()

        self.evaluate(False)

        root_shouted_number = self.monkeys['root'].shouted_number

        return root_shouted_number if root_shouted_number is not None else 0

    def part2(self) -> int:
        self.z3_solver = Solver()

        humn_int = Int('humn')

        self.monkeys['humn'].shouted_number = humn_int
        self.monkeys['root'].op = '='

        self.evaluate(True)

        self.z3_solver.check()

        return self.z3_solver.model().eval(humn_int)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'root: pppw + sjmn',
                    'dbpl: 5',
                    'cczh: sllz + lgvd',
                    'zczc: 2',
                    'ptdq: humn - dvpt',
                    'dvpt: 3',
                    'lfqf: 4',
                    'humn: 5',
                    'ljgn: 2',
                    'sjmn: drzm * dbpl',
                    'sllz: 4',
                    'pppw: cczh / lfqf',
                    'lgvd: ljgn * ptdq',
                    'drzm: hmdt - zczc',
                    'hmdt: 32',
                ],
                'part1': 152,
                'part2': 301,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 38731621732448
        self.common(input_data)
        assert self.part2() == 3848301405790

        return len(tests) + 1
