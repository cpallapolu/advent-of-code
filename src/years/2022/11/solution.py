

from math import prod

from aocpuzzle import AoCPuzzle
from years.utils.common import strip_lines

ADD_OP = '+'
MULTIPLY_OP = '*'


class Monkey:
    def __init__(self, monkey_data: str) -> None:
        self.parse_monkey(monkey_data)
        self.inspected_items = 0

    def parse_monkey(self, monkey_data: str):
        list_monkey_data = monkey_data.split('\n')

        self.num = int(list_monkey_data.pop(0).split().pop(-1)[:-1])
        self.items = list(map(int, list_monkey_data.pop(0).split(':').pop(-1).strip().split(', ')))
        self.op, self.op_val = list_monkey_data.pop(0).split()[-2:]
        self.div_by = int(list_monkey_data.pop(0).split().pop(-1))
        self.throw_to = (
            int(list_monkey_data.pop(0).split().pop(-1)),
            int(list_monkey_data.pop(0).split().pop(-1)),
        )

    def __str__(self) -> str:
        return ', '.join([
            f'items: {str(self.items)}',
            f'op: {self.op}',
            f'op_val: {self.op_val}',
            f'div_by: {str(self.div_by)}',
            f'throw_to: {str(self.throw_to)}',
        ])


class Puzzle11(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        input_data = strip_lines(input_data)
        self.monkeys = {}

        for monkey in '\n'.join(input_data).split('\n\n'):
            parsed_monkey = Monkey(monkey)
            self.monkeys[parsed_monkey.num] = parsed_monkey

    def calculate_worry_level(self, worry_level: int, op: str, op_val: str) -> int:
        actual_op_val = worry_level if op_val == 'old' else int(op_val)

        return sum([worry_level, actual_op_val]) if op == ADD_OP else prod([worry_level, actual_op_val])

    def simulate_rounds(self, rounds: int, div_or_mod: str, div_or_mod_val: int) -> int:
        for _ in range(rounds):
            for monkey in self.monkeys.values():
                while len(monkey.items) > 0:
                    item = monkey.items.pop(0)
                    monkey.inspected_items += 1

                    new_worry_level = eval(
                        ' '.join([
                            str(self.calculate_worry_level(item, monkey.op, monkey.op_val)),
                            div_or_mod,
                            str(div_or_mod_val),
                        ]),
                    )

                    target_monkey = monkey.throw_to[new_worry_level % monkey.div_by != 0]
                    self.monkeys[target_monkey].items.append(new_worry_level)

        return prod(sorted(monkey.inspected_items for monkey in self.monkeys.values())[-2:])

    def part1(self) -> int:
        return self.simulate_rounds(20, '//', 3)

    def part2(self) -> int:
        modulo = prod(monkey.div_by for monkey in self.monkeys.values())

        return self.simulate_rounds(10000, '%', modulo)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'Monkey 0:',
                    'Starting items: 79, 98',
                    'Operation: new= old * 19',
                    'Test: divisible by 23',
                    'If true: throw to monkey 2',
                    'If false: throw to monkey 3',
                    '',
                    'Monkey 1:',
                    'Starting items: 54, 65, 75, 74',
                    'Operation: new= old + 6',
                    'Test: divisible by 19',
                    'If true: throw to monkey 2',
                    'If false: throw to monkey 0',
                    '',
                    'Monkey 2:',
                    'Starting items: 79, 60, 97',
                    'Operation: new= old * old',
                    'Test: divisible by 13',
                    'If true: throw to monkey 1',
                    'If false: throw to monkey 3',
                    '',
                    'Monkey 3:',
                    'Starting items: 74',
                    'Operation: new= old + 3',
                    'Test: divisible by 17',
                    'If true: throw to monkey 0',
                    'If false: throw to monkey 1',
                ],
                'part1': 10605,
                'part2': 2713310158,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 58056
        self.common(input_data)
        assert self.part2() == 15048718170

        return len(tests) + 1
