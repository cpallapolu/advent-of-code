

from aocpuzzle import AoCPuzzle
from years.utils.common import strip_lines


class Puzzle04(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        input_data = strip_lines(input_data)
        self.assignments = []
        for pair in input_data:
            first_start, first_end, second_start, second_end = list(
                map(int, pair.replace(',', ' ').replace('-', ' ').split()),
            )

            self.assignments.append([
                set(range(first_start, first_end + 1)),
                set(range(second_start, second_end + 1)),
            ])

    def part1(self) -> int:
        return sum(
            1 if first.issubset(second) or second.issubset(first) else 0
            for first, second in self.assignments
        )

    def part2(self) -> int:
        return sum(
            1 if(first.intersection(second) or second.intersection(first)) else 0
            for first, second in self.assignments
        )

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '2-4,6-8',
                    '2-3,4-5',
                    '5-7,7-9',
                    '2-8,3-7',
                    '6-6,4-6',
                    '2-6,4-8',
                ],
                'part1': 2,
                'part2': 4,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 464
        self.common(input_data)
        assert self.part2() == 770

        return len(tests) + 1
