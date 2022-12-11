

from math import prod

from aocpuzzle import AoCPuzzle

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
        self.test_divisible_by = int(list_monkey_data.pop(0).split().pop(-1))
        self.test_true_monkey = int(list_monkey_data.pop(0).split().pop(-1))
        self.test_false_monkey = int(list_monkey_data.pop(0).split().pop(-1))

    def __str__(self) -> str:
        return ', '.join([
            f'items: {str(self.items)}',
            f'op: {self.op}',
            f'op_val: {self.op_val}',
            f'divisible_by: {str(self.test_divisible_by)}',
            f'true_monkey: {str(self.test_true_monkey)}',
            f'false_monkey: {str(self.test_false_monkey)}',
        ])


class Puzzle11(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.monkeys = {}

        for monkey in '\n'.join(input_data).split('\n\n'):
            parsed_monkey = Monkey(monkey)
            self.monkeys[parsed_monkey.num] = parsed_monkey

    def calculate_new_worry_level(self, worry_level: int, op: str, op_val: str) -> int:
        actual_op_val = worry_level if op_val == 'old' else int(op_val)

        return eval(f'{worry_level} {op} {actual_op_val}')

    def simulate_round(self, monkey: Monkey, relief_val: int) -> None:
        print()
        while len(monkey.items) > 0:
            item = monkey.items.pop(0)
            monkey.inspected_items += 1

            new_worry_level = self.calculate_new_worry_level(item, monkey.op, monkey.op_val) // relief_val
            target_monkey = (
                monkey.test_true_monkey
                if new_worry_level % monkey.test_divisible_by == 0
                else monkey.test_false_monkey
            )

            self.monkeys[target_monkey].items.append(new_worry_level)

            # print('item::', item, new_worry_level, new_worry_level % monkey.test_divisible_by, target_monkey)

    def part1(self) -> int:
        for _ in range(0, 20):
            for monkey in self.monkeys.values():
                self.simulate_round(monkey, 3)

        return prod(sorted(monkey.inspected_items for monkey in self.monkeys.values())[-2:])

    def part2(self) -> int:
        for _ in range(0, 10000):
            for monkey in self.monkeys.values():
                self.simulate_round(monkey, 1)

        print(prod(sorted(monkey.inspected_items for monkey in self.monkeys.values())[-2:]))
        return prod(sorted(monkey.inspected_items for monkey in self.monkeys.values())[-2:])

    def test_cases(self, input_data: list[str]) -> int:
        print('day11 test_cases in day11')
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
        assert self.part1() == 1
        self.common(input_data)
        assert self.part2() == 2

        return len(tests) + 1
