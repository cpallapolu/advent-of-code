from collections import defaultdict
from typing import Dict, List

from aocpuzzle import AoCPuzzle


class Puzzle10(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.adapters = list(map(int, input_data))
        self.max_rating = max(self.adapters)
        self.target_rating = self.max_rating + 3

    def part1(self) -> int:
        adapters = self.adapters[:]
        curr_rating = 0

        adapters_left = set()
        adapters_left.add(0)

        diff_1, diff_3 = 0, 0

        while len(adapters_left) > 0:
            rating = adapters_left.pop()

            for next_rating_option in [rating + idx for idx in range(1, 4)]:
                if next_rating_option in adapters:
                    difference = next_rating_option - curr_rating
                    curr_rating = next_rating_option

                    if difference == 1:
                        diff_1 += 1

                    if difference == 3 or curr_rating + 3 == self.target_rating:
                        diff_3 += 1

                    adapters.remove(next_rating_option)
                    adapters_left.add(next_rating_option)
        return diff_1 * diff_3

    def count_ways(self, curr_rating: int) -> int:
        if curr_rating in self.cache:
            return self.cache[curr_rating]

        if curr_rating == self.target_rating:
            return 1

        count = 0

        for next_rating in [a for a in self.adapters if 1 <= a - curr_rating <= 3]:
            count += self.count_ways(next_rating)

        self.cache[curr_rating] = count

        return count

    def part2(self) -> int:
        curr_rating = 0
        self.cache: Dict[int, int] = defaultdict(int)
        self.adapters = self.adapters[:] + [self.target_rating]

        return self.count_ways(curr_rating)

    def test_cases(self, input_data: List[str]) -> int:
        part1_tests_1 = ['16', '10', '15', '5', '1', '11', '7', '19', '6', '12', '4']
        part1_tests_2 = [
            '28', '33', '18', '42', '31', '14', '46', '20', '48', '47', '24', '23', '49',
            '45', '19', '38', '39', '11', '1', '32', '25', '35', '8', '17', '7', '9', '4',
            '2', '34', '10', '3',
        ]

        self.common(part1_tests_1)
        assert self.part1() == 28
        assert self.part2() == 8

        self.common(part1_tests_2)
        assert self.part1() == 220
        assert self.part2() == 19208

        self.common(input_data)
        assert self.part1() == 2775
        assert self.part2() == 518344341716992

        return 3
