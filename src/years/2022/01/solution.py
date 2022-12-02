
from aocpuzzle import AoCPuzzle


class Puzzle01(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        elves_calories: list[int] = [0]

        for calories in input_data:
            if len(calories) == 0:
                elves_calories.append(0)
                continue

            elves_calories[-1] += int(calories)

        self.calories = sorted(elves_calories, reverse=True)

    def part1(self) -> int:
        return self.calories[0]

    def part2(self) -> int:
        return sum(self.calories[:3])

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

        self.common(input_data)
        assert self.part1() == 69528
        self.common(input_data)
        assert self.part2() == 206152

        return len(tests) + 1
