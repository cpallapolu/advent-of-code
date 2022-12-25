

from aocpuzzle import AoCPuzzle


class Puzzle25(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.input_data = [line.strip() for line in input_data]
        self.place_values = '=-012'

    def parse_snafu(self, snafu: str) -> int:
        place = 1
        total = 0

        for char in snafu[::-1]:
            total += (self.place_values.index(char) - 2) * place
            place *= 5

        return total

    def to_snafu(self, num: int) -> str:
        snafu = ''
        while num > 0:
            num, place = divmod(num + 2, 5)
            snafu += self.place_values[place]

        return snafu[::-1]

    def part1(self) -> str:
        self.totals = sum([self.parse_snafu(snafu) for snafu in self.input_data])

        ans = self.to_snafu(self.totals)
        return ans

    def part2(self) -> str:
        return 'There is no part two!'

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '1=-0-2',
                    '12111',
                    '2=0=',
                    '21',
                    '2=01',
                    '111',
                    '20012',
                    '112',
                    '1=-1=',
                    '1-12',
                    '12',
                    '1=',
                    '122',
                ],
                'part1': '2=-1=0',
                'part2': 'There is no part two!',
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            assert self.totals == 4890
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == '2=0=02-0----2-=02-10'
        assert self.totals == 30223327868980
        self.common(input_data)
        assert self.part2() == 'There is no part two!'

        return len(tests) + 1
