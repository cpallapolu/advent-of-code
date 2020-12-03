from typing import List, Set

from aocpuzzle import AoCPuzzle


class Puzzle01(AoCPuzzle):
    def post_process_input_data(self, input_data: List[str]) -> List[int]:
        return [int(num) for num in input_data]

    def common(self, input_data: List[int]) -> None:
        self.target = 2020
        self.count_set: Set = set()

    def part1(self, input_data: List[int]) -> int:
        product = -1

        for num in input_data:
            rest_of_sum = self.target - num

            if rest_of_sum in self.count_set:
                product = num * rest_of_sum
                break
            self.count_set.add(num)

        return product

    def part2(self, input_data: List[int]) -> int:
        for i in range(len(input_data) - 1):
            curr_set = set()
            curr_sum = self.target - input_data[i]

            for j in range(i + 1, len(input_data)):
                if (curr_sum - input_data[j]) in curr_set:
                    return input_data[i] * input_data[j] * (curr_sum - input_data[j])

                curr_set.add(input_data[j])
        return -1

    def test_cases(self, input_data: List[int]) -> int:
        expenses = [1721, 979, 366, 299, 675, 1456]

        assert self.part1(expenses) == 514579
        assert self.part1(input_data) == 651651

        assert self.part2(expenses) == 241861950
        assert self.part2(input_data) == 214486272

        return 2
