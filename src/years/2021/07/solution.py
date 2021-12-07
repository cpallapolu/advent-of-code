

from aocpuzzle import AoCPuzzle


class Puzzle07(AoCPuzzle):
    def common(self, input_data: str) -> None:
        self.positions = list(map(int, input_data.split(',')))

    def calculate_fuel(self, is_linear: bool) -> int:
        len_positions = len(self.positions)
        linear_fuels = [0] * len_positions
        non_linear_fuels = [0] * len_positions

        for idx in range(len_positions):
            for position in self.positions:
                move = abs(position - idx)

                linear_fuels[idx] += move
                non_linear_fuels[idx] += (move * (move + 1)) // 2

        return min(linear_fuels) if is_linear else min(non_linear_fuels)

    def part1(self) -> int:
        return self.calculate_fuel(True)

    def part2(self) -> int:
        return self.calculate_fuel(False)

    def test_cases(self, input_data: str) -> int:
        tests = [
            '16,1,2,0,4,2,7,1,2,14',
        ]

        for test in tests:
            self.common(test)
            assert self.part1() == 37
            self.common(test)
            assert self.part2() == 168

        self.common(input_data)
        assert self.part1() == 340056
        self.common(input_data)
        assert self.part2() == 96592275

        return len(tests) + 1

    def part1_median(self) -> int:
        median = sorted(self.positions)[len(self.positions) // 2]

        return sum(abs(position - median) for position in self.positions)

    def part1_alter(self) -> int:
        sorted_positions = sorted(self.positions)

        left, right = 0, len(sorted_positions) - 1
        fuel = 0

        while left < right:
            fuel += (sorted_positions[right] - sorted_positions[left])

            right -= 1
            left += 1

        return fuel
