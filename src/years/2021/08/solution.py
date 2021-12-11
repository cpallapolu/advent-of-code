

from aocpuzzle import AoCPuzzle


class SignalEntry:
    def __init__(self, signal_pattern: str, four_digits: str) -> None:
        self.signal_pattern = signal_pattern.split()
        self.four_digits = four_digits.split()
        self.digits: list[set[str]] = [set()] * 10

        self.build_digits()

    def build_digits(self) -> None:
        self.digits[1] = next(set(sp) for sp in self.signal_pattern if len(sp) == 2)
        self.digits[4] = next(set(sp) for sp in self.signal_pattern if len(sp) == 4)
        self.digits[7] = next(set(sp) for sp in self.signal_pattern if len(sp) == 3)
        self.digits[8] = next(set(sp) for sp in self.signal_pattern if len(sp) == 7)

        five_lens = (set(sp) for sp in self.signal_pattern if len(sp) == 5)

        for five_len in five_lens:
            if self.digits[1].issubset(five_len):
                self.digits[3] = five_len
            elif len(self.digits[4] & five_len) == 3:
                self.digits[5] = five_len
            else:
                self.digits[2] = five_len

        six_lens = (set(sp) for sp in self.signal_pattern if len(sp) == 6)

        for six_len in six_lens:
            if len(six_len & self.digits[4]) == 4:
                self.digits[9] = six_len
            elif len(six_len & self.digits[5]) == 5:
                self.digits[6] = six_len
            else:
                self.digits[0] = six_len

    def get_digit_value(self, mapping: str) -> int:
        return self.digits.index(set(mapping))


class Puzzle08(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.signal_entries = [
            SignalEntry(*' '.join(entry.split()).split(' | '))
            for entry in input_data
        ]

    def part1(self) -> int:
        digits_1478 = 0

        for signal_entry in self.signal_entries:
            value = 0

            for four_digit in signal_entry.four_digits:
                value = value * 10 + signal_entry.get_digit_value(four_digit)

                if value % 10 in (1, 4, 7, 8):
                    digits_1478 += 1

        return digits_1478

    def part2(self) -> int:
        output_sum = 0

        for signal_entry in self.signal_entries:
            value = 0

            for four_digit in signal_entry.four_digits:
                value = value * 10 + signal_entry.get_digit_value(four_digit)

            output_sum += value

        return output_sum

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb \
                    | fdgacbe cefdb cefbgd gcbe',
                    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec \
                    | fcgedb cgb dgebacf gc',
                    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef \
                    | cg cg fdcagb cbg',
                    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega \
                    | efabcd cedba gadfec cb',
                    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga \
                    | gecf egdcabf bgf bfgea',
                    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf \
                    | gebdcfa ecba ca fadegcb',
                    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf \
                    | cefg dcbef fcge gbcadfe',
                    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd \
                    | ed bcgafe cdgba cbgef',
                    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg \
                    | gbdfcae bgc cg cgb',
                    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc \
                    | fgae cfgab fg bagce',
                ],
                'part1': 26,
                'part2': 61229,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 362
        self.common(input_data)
        assert self.part2() == 1020159

        return len(tests) + 1
