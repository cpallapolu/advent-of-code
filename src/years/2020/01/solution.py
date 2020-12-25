from typing import List, Set

from aocpuzzle import AoCPuzzle


class Puzzle01(AoCPuzzle):
    def common(self, input_data: List[int]) -> None:
        self.target = 2020
        self.nums = [int(num) for num in input_data]

    def part1(self, input_data: List[int]) -> int:
        product = -1
        count_set: Set = set()

        for num in self.nums:
            rest_of_sum = self.target - num

            if rest_of_sum in count_set:
                product = num * rest_of_sum
                break

            count_set.add(num)

        return product

    def part2(self, input_data: List[int]) -> int:
        for i in range(len(self.nums) - 1):
            curr_set = set()
            curr_sum = self.target - self.nums[i]

            for j in range(i + 1, len(self.nums)):
                if (curr_sum - self.nums[j]) in curr_set:
                    return self.nums[i] * self.nums[j] * (curr_sum - self.nums[j])

                curr_set.add(self.nums[j])
        return -1

    def test_cases(self, input_data: List[int]) -> int:
        expenses = [1721, 979, 366, 299, 675, 1456]

        self.common(expenses)
        assert self.part1(expenses) == 514579
        self.common(input_data)
        assert self.part1(input_data) == 651651

        self.common(expenses)
        assert self.part2(expenses) == 241861950
        self.common(input_data)
        assert self.part2(input_data) == 214486272

        return 2
