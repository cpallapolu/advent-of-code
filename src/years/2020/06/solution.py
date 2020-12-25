from collections import Counter
from typing import List

from aocpuzzle import AoCPuzzle


class Puzzle06(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.group_answers = []

        for group in '\n'.join(input_data).split('\n\n'):
            self.group_answers.append((
                len(group.split('\n')),
                Counter(''.join(group.split('\n'))),
            ))

    def part1(self) -> int:
        return sum(
            len(group_answer.keys())
            for _, group_answer in self.group_answers
        )

    def part2(self) -> int:
        return sum(
            1
            for group_count, group_answer in self.group_answers
            for counts in group_answer.values()
            if counts == group_count
        )

    def test_cases(self, input_data: List[str]) -> int:
        tests = ['abc', '', 'a', 'b', 'c', '', 'ab', 'ac', '', 'a', 'a', 'a', 'a', '', 'b']
        total_tests = 0

        self.common(tests)
        total_tests += len(self.group_answers)
        assert self.part1() == 11

        self.common(input_data)
        assert self.part1() == 6782

        self.common(tests)
        total_tests += len(self.group_answers)
        assert self.part2() == 6

        self.common(input_data)
        assert self.part2() == 3596

        total_tests += len(self.group_answers)

        return total_tests
