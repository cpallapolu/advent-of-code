

from functools import cmp_to_key
from math import prod
from typing import Union

from aocpuzzle import AoCPuzzle

pair_type = Union[list[int], int]


class Puzzle13(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.pairs = []
        self.packets = []

        for packet in range(0, len(input_data), 3):
            pair = list(map(eval, input_data[packet:packet + 2]))
            self.pairs.append(pair)
            self.packets.extend(pair)

        self.divider_packet_2 = [[2]]
        self.divider_packet_6 = [[6]]

        self.packets.append(self.divider_packet_2)
        self.packets.append(self.divider_packet_6)

    def is_left_val_smaller(self, left: int, right: int) -> int:
        return (left > right) - (left < right)

    def compare_list_packets(self, left: list[int], right: list[int]) -> int:
        for left_val, right_val in zip(left, right):
            is_left_val_smaller = self.compare_packets(left_val, right_val)

            if is_left_val_smaller != 0:
                return is_left_val_smaller

        return self.compare_packets(len(left), len(right))

    def compare_packets(self, left: pair_type, right: pair_type) -> int:
        if type(left) == int and type(right) == int:
            return self.is_left_val_smaller(left, right)

        left_list: list[int] = left if isinstance(left, list) else [left]
        right_list: list[int] = right if isinstance(right, list) else [right]

        return self.compare_list_packets(left_list, right_list)

    def part1(self) -> int:
        return sum([
            idx
            for idx, pair in enumerate(self.pairs, 1)
            if self.compare_packets(pair[0], pair[1]) == -1
        ])

    def part2(self) -> int:
        sorted_packets = sorted(self.packets, key=cmp_to_key(self.compare_packets))

        return prod([
            sorted_packets.index(self.divider_packet_2) + 1,
            sorted_packets.index(self.divider_packet_6) + 1,
        ])

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '[1, 1, 3, 1, 1]',
                    '[1, 1, 5, 1, 1]',
                    '',
                    '[[1], [2, 3, 4]]',
                    '[[1], 4]',
                    '',
                    '[9]',
                    '[[8, 7, 6]]',
                    '',
                    '[[4, 4], 4, 4]',
                    '[[4, 4], 4, 4, 4]',
                    '',
                    '[7, 7, 7, 7]',
                    '[7, 7, 7]',
                    '',
                    '[]',
                    '[3]',
                    '',
                    '[[[]]]',
                    '[[]]',
                    '',
                    '[1, [2, [3, [4, [5, 6, 7]]]], 8, 9]',
                    '[1, [2, [3, [4, [5, 6, 0]]]], 8, 9]',
                ],
                'part1': 13,
                'part2': 140,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 5825
        self.common(input_data)
        assert self.part2() == 24477

        return len(tests) + 1
