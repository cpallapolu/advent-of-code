from typing import List, Tuple

from aocpuzzle import AoCPuzzle


class Puzzle13(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.your_departure = int(input_data[0])
        self.buses = list(map(lambda b: int(b) if b != 'x' else None, input_data[1].split(',')))

    def part1(self, input_data: List[str]) -> int:
        wait_times = [
            (bus, bus - (self.your_departure % bus))
            for bus in self.buses
            if bus is not None
        ]

        bus_id, wait_time = min(wait_times, key=lambda nb: nb[1])

        return bus_id * wait_time

    def chinese_remainder(self, divs_and_rems: List[Tuple[int, int]]) -> int:
        # 1. Get product of all divisors
        prod = 1

        for divisor, _ in divs_and_rems:
            prod *= divisor

        total = 0

        for divisor, remainder in divs_and_rems:
            # 2. Get partial product of each divisor
            partial_prod = prod // divisor

            # 3. Find out the Modular multiplicative inverse of partial_prod under modulo divisor
            # ref: https://docs.python.org/3/whatsnew/3.8.html
            inverse = pow(partial_prod, -1, divisor)

            # 4. Adding the result product
            total += remainder * partial_prod * inverse

        # 5. Return the smallest solution
        return total % prod

    def part2(self, input_data: List[str]) -> int:
        divisors_and_remainders = [
            (bus, bus - idx)
            for idx, bus in enumerate(self.buses)
            if bus is not None
        ]

        return self.chinese_remainder(divisors_and_remainders)

    def test_cases(self, input_data: List[str]) -> int:

        self.common(['939', '7,13,x,x,59,x,31,19'])
        assert self.part1(['939', '7,13,x,x,59,x,31,19']) == 295

        self.common(['1', '17,x,13,19'])
        assert self.part2(['1', '17,x,13,19']) == 3417

        self.common(['1', '67,7,59,61'])
        assert self.part2(['1', '67,7,59,61']) == 754018

        self.common(['1', '67,x,7,59,61'])
        assert self.part2(['1', '67,x,7,59,61']) == 779210

        self.common(['1', '67,7,x,59,61'])
        assert self.part2(['1', '67,7,x,59,61']) == 1261476

        self.common(['1', '1789,37,47,1889'])
        assert self.part2(['1', '1789,37,47,1889']) == 1202161486

        self.common(input_data)
        assert self.part1(input_data) == 2845
        assert self.part2(input_data) == 487905974205117

        return 2
