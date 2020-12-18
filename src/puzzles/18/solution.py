
import re

from typing import List, Match

from aocpuzzle import AoCPuzzle

OP_ADD = '+'
OP_MUL = '*'
OP_PAREN = '('


class Puzzle18(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.expressions = [expression.replace(' ', '') for expression in input_data]

        self.PAREN_REGEX = re.compile(r'\(([^()]+)\)')

        self.ADD_REGEX = re.compile(r'^(\d+)\+(\d+)')
        self.ADD_PRECEDENCE_REGEX = re.compile(r'(\d+)\+(\d+)')

        self.MUL_REGEX = re.compile(r'^(\d+)\*(\d+)')
        self.MUL_PRECEDENCE_REGEX = re.compile(r'(\d+)\*(\d+)')

    def eval_expr(self, match: Match[str], op: str) -> str:
        a, b = int(match.group(1)), int(match.group(2))

        return str(a + b) if op == '+' else str(a * b)

    def eval_val(self, expression: str, precedence: bool, op: str) -> str:
        regex = (
            self.ADD_REGEX
            if op == OP_ADD and precedence is False
            else self.ADD_PRECEDENCE_REGEX
            if op == OP_ADD and precedence is True
            else self.MUL_REGEX
            if op == OP_MUL and precedence is False
            else self.MUL_PRECEDENCE_REGEX
        )

        return re.sub(regex, lambda m: self.eval_expr(m, op), expression)

    def eval_paren(self, expression: str, precedence: bool) -> str:
        return re.sub(
            self.PAREN_REGEX,
            lambda m: str(self.evaluate(m.group(1), precedence)),
            expression,
        )

    def evaluate(self, expression: str, precedence: bool) -> int:
        while '(' in expression:
            expression = self.eval_paren(expression, precedence)

        if precedence is False:
            while '+' in expression or '*' in expression:
                expression = self.eval_val(expression, precedence, OP_ADD)
                expression = self.eval_val(expression, precedence, OP_MUL)
        else:
            while '+' in expression:
                expression = self.eval_val(expression, precedence, '+')
            while '*' in expression:
                expression = self.eval_val(expression, precedence, '*')

        return int(expression)

    def part1(self, input_data: List[str]) -> int:
        return sum(self.evaluate(expression, False) for expression in self.expressions)

    def part2(self, input_data: List[str]) -> int:
        return sum(self.evaluate(expression, True) for expression in self.expressions)

    def test_cases(self, input_data: List[str]) -> int:
        tests = ['1 + 2 * 3 + 4 * 5 + 6']
        self.common(tests)
        assert self.part1(tests) == 71
        assert self.part2(tests) == 231

        tests = ['1 + (2 * 3) + (4 * (5 + 6))']
        self.common(tests)
        assert self.part1(tests) == 51
        assert self.part2(tests) == 51

        tests = ['2 * 3 + (4 * 5)']
        self.common(tests)
        assert self.part1(tests) == 26
        assert self.part2(tests) == 46

        tests = ['5 + (8 * 3 + 9 + 3 * 4 * 3)']
        self.common(tests)
        assert self.part1(tests) == 437
        assert self.part2(tests) == 1445

        tests = ['5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))']
        self.common(tests)
        assert self.part1(tests) == 12240
        assert self.part2(tests) == 669060

        tests = ['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2']
        self.common(tests)
        assert self.part1(tests) == 13632
        assert self.part2(tests) == 23340

        self.common(input_data)
        assert self.part1(tests) == 3885386961962
        assert self.part2(tests) == 112899558798666

        return 7
