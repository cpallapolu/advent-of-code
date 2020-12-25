from itertools import combinations
from typing import Any, List

from aocpuzzle import AoCPuzzle


class Puzzle09(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.preamble_length = 25
        self.nums = list(map(int, input_data))

    def part1(self) -> int:
        for idx, num in enumerate(self.nums[self.preamble_length:]):
            is_valid = False
            for x, y in combinations(self.nums[idx:idx + self.preamble_length], 2):
                if x + y == num:
                    is_valid = True
                    break

            if is_valid is False:
                break

        self.invalid_num = num

        return self.invalid_num

    def part2(self) -> int:
        min_num, max_num = 0, 0

        for idx in range(len(self.nums)):
            continuous_list = [self.nums[idx]]
            next_idx = 0

            while sum(continuous_list) < self.invalid_num:
                next_idx += 1
                continuous_list.append(self.nums[idx + next_idx])

            if sum(continuous_list) == self.invalid_num:
                min_num, max_num = min(continuous_list), max(continuous_list)
                break

        return min_num + max_num

    def test_cases(self, input_data: Any) -> int:
        tests = [
            '35', '20', '15', '25', '47', '40', '62', '55', '65', '95', '102', '117', '150',
            '182', '127', '219', '299', '277', '309', '576',
        ]

        self.common(tests)
        self.preamble_length = 5
        assert self.part1() == 127
        assert self.part2() == 62

        self.common(input_data)
        assert self.part1() == 1930745883
        assert self.part2() == 268878261

        return 2
