

from string import ascii_letters

from aocpuzzle import AoCPuzzle


class Puzzle03(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.rucksacks = []

        for data in input_data:
            half_len = len(data) // 2
            first, second = data[:half_len], data[half_len:]
            self.rucksacks.append((set(first), set(second)))

        self.groups = [
            [set(group) for group in input_data[idx:idx + 3]]
            for idx in range(0, len(input_data), 3)
        ]

    def part1(self) -> int:
        return sum(
            ascii_letters.index(first.intersection(second).pop()) + 1
            for first, second in self.rucksacks
        )

    def part2(self) -> int:
        return sum(
            ascii_letters.index(set.intersection(*group).pop()) + 1
            for group in self.groups
        )

    def test_cases(self, input_data: list[str]) -> int:
        print('day03 test_cases in day03')
        tests: list[dict] = [
            {
                'input_data': [
                    'vJrwpWtwJgWrhcsFMMfFFhFp',
                    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
                    'PmmdzqPrVvPwwTWBwg',
                    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
                    'ttgJtRGJQctTZtZT',
                    'CrZsJsPPZsGzwwsLwLmpwMDw',
                ],
                'part1': 157,
                'part2': 70,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 7889
        self.common(input_data)
        assert self.part2() == 2825

        return len(tests) + 1
