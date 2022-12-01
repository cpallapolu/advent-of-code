

from collections import defaultdict

from aocpuzzle import AoCPuzzle


class Puzzle01(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.elves = 0
        self.calories: dict[int, int] = defaultdict(int)

        for calories in input_data:
            if len(calories) == 0:
                self.elves += 1
                continue

            self.calories[self.elves] += int(calories)

    def part1(self) -> int:
        return max(self.calories.values())

    def part2(self) -> int:
        return sum(sorted(self.calories.values(), reverse=True)[:3])

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '1000',
                    '2000',
                    '3000',
                    '',
                    '4000',
                    '',
                    '5000',
                    '6000',
                    '',
                    '7000',
                    '8000',
                    '9000',
                    '',
                    '10000',
                ],
                'part1': 24000,
                'part2': 45000,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        return len(tests) + 1
