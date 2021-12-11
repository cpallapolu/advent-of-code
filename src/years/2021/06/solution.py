

from typing import Counter

from aocpuzzle import AoCPuzzle


class Puzzle06(AoCPuzzle):
    def common(self, input_data: str) -> None:
        # for part1 list would have sufficed but as the days increase the arrray size will get
        # out of hand and will slow the process. That's why we need dictionary for easy access.
        self.fishes = Counter(map(int, input_data.split(',')))

    def reproduce(self, days: int, fishes: dict[int, int]) -> int:
        for _ in range(days):
            state_after_day = {
                internal_timer - 1: count
                for internal_timer, count in fishes.items()
            }

            # removing fishes that reproduced
            state_after_day.pop(-1, None)

            # if we have any fishes with 0 timer left,
            # we add a new fishes equal to the number of fishes with 0 timer
            # then we reset the timer of these fishes to 6
            if 0 in fishes:
                state_after_day[8] = fishes[0]
                state_after_day[6] = fishes[0] + state_after_day.get(6, 0)

            fishes = state_after_day

        return sum(fishes.values())

    def part1(self) -> int:
        return self.reproduce(80, self.fishes)

    def part2(self) -> int:
        return self.reproduce(256, self.fishes)

    def test_cases(self, input_data: str) -> int:
        tests: list[dict] = [
            {
                'input_data': '3,4,3,1,2',
                'part1': 5934,
                'part2': 26984457539,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 360610
        self.common(input_data)
        assert self.part2() == 1631629590423

        return len(tests) + 1
