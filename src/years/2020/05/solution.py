from typing import List

from aocpuzzle import AoCPuzzle


class Puzzle05(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.seat_ids = [
            int(
                x.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'),
                base=2,
            )
            for x in input_data
        ]

    def part1(self) -> int:
        return max(self.seat_ids)

    def part2(self) -> int:
        missing_seats = [
            idx
            for idx in range(self.part1())
            if idx not in self.seat_ids
        ]

        for ms in missing_seats:
            if ms - 1 not in missing_seats and ms + 1 not in missing_seats:
                return ms
        return 0

    def test_cases(self, input_data: List[str]) -> int:
        tests = ['FBFBBFFRLR', 'BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']

        self.common(tests)
        assert self.seat_ids == [357, 567, 119, 820]
        assert self.part1() == 820

        self.common(input_data)
        assert self.part1() == 959

        self.common(input_data)
        assert self.part2() == 527

        return 2
