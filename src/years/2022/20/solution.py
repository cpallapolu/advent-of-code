

from aocpuzzle import AoCPuzzle


class Puzzle20(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.encrypted_file = list(map(int, input_data))

    def decrypt(self, mix_times: int) -> list[tuple[int, int]]:
        original_sequence = list(enumerate(self.encrypted_file))
        new_sequence = original_sequence[:]

        for _ in range(mix_times):
            for (original_idx, original_num) in original_sequence:
                idx_in_new_sequence = new_sequence.index((original_idx, original_num))

                new_sequence.remove((original_idx, original_num))

                target_idx = (idx_in_new_sequence + original_num) % len(new_sequence)

                new_sequence.insert(target_idx, (original_idx, original_num))

        return new_sequence

    def score(self, sequence: list[tuple[int, int]]) -> int:
        len_sequence = len(sequence)

        values = [p[1] for p in sequence]
        zero_pos = values.index(0)

        return sum(
            values[(zero_pos + (idx * 1000)) % len_sequence]
            for idx in range(1, 4)
        )

    def part1(self) -> int:
        return self.score(self.decrypt(1))

    def part2(self) -> int:
        self.encrypted_file = self.encrypted_file[:]
        self.encrypted_file = [num * 811589153 for num in self.encrypted_file]

        return self.score(self.decrypt(10))

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '1',
                    '2',
                    '-3',
                    '3',
                    '-2',
                    '0',
                    '4',
                ],
                'part1': 3,
                'part2': 1623178306,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 19070
        self.common(input_data)
        assert self.part2() == 14773357352059

        return len(tests) + 1
