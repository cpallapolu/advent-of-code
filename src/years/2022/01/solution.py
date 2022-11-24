

from aocpuzzle import AoCPuzzle


class Puzzle01(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        print('day01 common in day01')

    def part1(self) -> int:
        print('day01 part 1 in day01')
        return 1

    def part2(self) -> int:
        print('day01 part 2 in day01')
        return 2

    def test_cases(self, input_data: list[str]) -> int:
        print('day01 test_cases in day01')
        tests: list[dict] = [
            {
                'input_data': [],
                'part1': 1,
                'part2': 2,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        return len(tests) + 1
