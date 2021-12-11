

from typing import Counter

from aocpuzzle import AoCPuzzle


class Puzzle03(AoCPuzzle):
    def get_bits_for_position(self, report: list[str], position: int) -> str:
        bits_for_position = ''

        for row in range(len(report)):
            bits_for_position += report[row][position]

        return bits_for_position

    def get_numbers_for_position(self, report: list[str], bit: str, position: int) -> list[str]:
        return [
            diagnostic_number
            for diagnostic_number in report
            if diagnostic_number[position] == bit

        ]

    def common(self, input_data: list[str]) -> None:
        self.report = input_data
        self.positions = len(input_data[0])

    def part1(self) -> int:
        gamma = ''
        epsilon = ''

        for position in range(self.positions):
            bits_for_position = self.get_bits_for_position(self.report, position)

            counter_bits = Counter(bits_for_position).most_common()

            gamma += counter_bits[0][0]
            epsilon += counter_bits[1][0]

        self.gamma = int(gamma, 2)
        self.epsilon = int(epsilon, 2)

        return self.gamma * self.epsilon

    def bit_criteria(self, report: list[str], most_common_bit: bool) -> int:
        position = 0
        int_most_common_bit = 0 if most_common_bit is True else 1

        while len(report) > 1:
            bits_for_position = self.get_bits_for_position(report, position)

            counter_bits = sorted(
                Counter(bits_for_position).items(),
                key=lambda i: (i[1], i[0]),
                reverse=True,
            )

            report = self.get_numbers_for_position(
                report,
                counter_bits[int_most_common_bit][0],
                position,
            )
            position += 1

        return int(report[0], 2)

    def part2(self) -> int:
        self.oxygen_generator_rating = self.bit_criteria(self.report, True)
        self.co2_scrubber_rating = self.bit_criteria(self.report, False)

        return self.oxygen_generator_rating * self.co2_scrubber_rating

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '00100', '11110', '10110', '10111', '10101', '01111',
                    '00111', '11100', '10000', '11001', '00010', '01010',
                ],
                'part1': 198,
                'gamma': 22,
                'epsilon': 9,
                'part2': 230,
                'oxygen_generator_rating': 23,
                'co2_scrubber_rating': 10,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            assert self.gamma == test['gamma']
            assert self.epsilon == test['epsilon']

            self.common(test['input_data'])
            assert self.part2() == test['part2']
            assert self.oxygen_generator_rating == test['oxygen_generator_rating']
            assert self.co2_scrubber_rating == test['co2_scrubber_rating']

            self.common(input_data)
            assert self.part1() == 2724524
            assert self.gamma == 3259
            assert self.epsilon == 836

            assert self.part2() == 2775870
            assert self.oxygen_generator_rating == 4023
            assert self.co2_scrubber_rating == 690
        return len(tests) + 1
