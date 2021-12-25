
from itertools import permutations
from math import ceil, floor

from aocpuzzle import AoCPuzzle

OPEN_BRACKET = '['
CLOSE_BRACKET = ']'


class PairAddition:
    def __init__(self, data: list[str]) -> None:
        self.pairs: list[list[str]] = [
            list(line.replace(',', ''))
            for line in data
        ]
        self.summed_value: list[str] = []
        self.max_magnitude = 0

    def add_all_pairs(self):
        self.summed_value = self.pairs[0]

        for pair in self.pairs[1:]:
            self.summed_value = self.reduce_number(['[', *self.summed_value, *pair, ']'])

    def add_two_pairs(self):
        for pair_one, pair_two in permutations(self.pairs, 2):
            self.summed_value = self.reduce_number(['[', *pair_one, *pair_two, ']'])

            self.max_magnitude = max(self.max_magnitude, self.magnitude())

    def reduce_number(self, pair: list[str]) -> list[str]:
        should_split = True

        while should_split is True:
            pair = self.explode(pair)
            pair, should_split = self.split(pair)

        return pair

    def explode(self, pair: list[str]) -> list[str]:
        stack: list[str] = []
        depth, to_add, last_digit = 0, 0, -1

        while len(pair) > 0:
            stack.append(pair.pop(0))

            if stack[-1] == OPEN_BRACKET:
                if depth < 4:
                    depth += 1
                else:
                    left = int(pair.pop(0))
                    right = int(pair.pop(0))
                    pair.pop(0)

                    if last_digit != -1:
                        stack[last_digit] = str(int(stack[last_digit]) + left + to_add)
                    to_add = right
                    stack[-1] = '0'
                    last_digit = len(stack) - 1
            elif stack[-1] == CLOSE_BRACKET:
                depth -= 1
            elif stack[-1].isdigit() is True:
                stack[-1] = str(int(stack[-1]) + to_add)
                to_add = 0
                last_digit = len(stack) - 1

        return stack

    def split(self, pair: list[str]) -> tuple[list[str], bool]:
        new_pair: list[str] = []

        while len(pair) > 0:
            char = pair.pop(0)
            if char.isdigit() is True and int(char) > 9:
                left, right = floor(int(char) / 2), ceil(int(char) / 2)
                new_pair.extend(('[', str(left), str(right), ']'))
                return new_pair + pair, True
            new_pair.append(char)
        return new_pair, False

    def magnitude(self) -> int:
        stack: list[str] = []

        for char in self.summed_value:
            if char == ']':
                right, left = int(stack.pop()), int(stack.pop())
                stack.append(str(left * 3 + right * 2))
            elif char.isdigit() is True:
                stack.append(char)

        return int(stack[0])


class Puzzle18(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.pair_addition = PairAddition(input_data)

    def part1(self) -> int:
        self.pair_addition.add_all_pairs()

        return self.pair_addition.magnitude()

    def part2(self) -> int:
        self.pair_addition.add_two_pairs()

        return self.pair_addition.max_magnitude

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
                    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
                    '[7,[5,[[3,8],[1,4]]]]',
                    '[[2,[2,2]],[8,[8,1]]]',
                    '[2,9]',
                    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
                    '[[[5,[7,4]],7],1]',
                    '[[[[4,2],2],6],[8,7]]',
                ],
                'part1': 3488,
                'part2': 3805,
            },
            {
                'input_data': [
                    '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
                    '[[[5,[2,8]],4],[5,[[9,9],0]]]',
                    '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
                    '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
                    '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
                    '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
                    '[[[[5,4],[7,7]],8],[[8,3],8]]',
                    '[[9,3],[[9,9],[6,[4,9]]]]',
                    '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
                    '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
                ],
                'part1': 4140,
                'part2': 3993,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 3816
        self.common(input_data)
        assert self.part2() == 4819

        return len(tests) + 1
