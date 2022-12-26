

from aocpuzzle import AoCPuzzle


class Puzzle06(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.data_stream = input_data

    def start_of_packet_marker(self, window_len: int) -> int:
        return next(
            idx + window_len
            for idx in range(len(self.data_stream))
            if len(set(self.data_stream[idx:idx + window_len])) == window_len
        )

    def part1(self) -> int:
        return self.start_of_packet_marker(4)

    def part2(self) -> int:
        return self.start_of_packet_marker(14)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': 'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
                'part1': 7,
                'part2': 19,
            },
            {
                'input_data': 'bvwbjplbgvbhsrlpgdmjqwftvncz',
                'part1': 5,
                'part2': 23,
            },
            {
                'input_data': 'nppdvjthqldpwncqszvftbrmjlhg',
                'part1': 6,
                'part2': 23,
            },
            {
                'input_data': 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
                'part1': 10,
                'part2': 29,
            },
            {
                'input_data': 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',
                'part1': 11,
                'part2': 26,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 1531
        self.common(input_data)
        assert self.part2() == 2518

        return len(tests) + 1
