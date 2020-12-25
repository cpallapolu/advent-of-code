from collections import defaultdict

from aocpuzzle import AoCPuzzle


class Puzzle15(AoCPuzzle):
    def common(self, input_data: str) -> None:
        self.starting_numbers = list(map(int, input_data.split(',')))
        self.spoken_numbers = defaultdict(list)

        for self.turn, self.starting_number in enumerate(self.starting_numbers, start=1):
            self.spoken_numbers[self.starting_number].append(self.turn)

    def take_turns(self, last_turn: int) -> int:
        while self.turn < last_turn:
            self.turn += 1

            spoken_number = 0

            if len(self.spoken_numbers[self.starting_number]) >= 2:
                prev1, prev2 = self.spoken_numbers[self.starting_number][-2:]
                spoken_number = prev2 - prev1

            self.spoken_numbers[spoken_number].append(self.turn)
            self.starting_number = spoken_number

        return self.starting_number

    def part1(self, input_data: str) -> int:
        return self.take_turns(2020)

    def part2(self, input_data: str) -> int:
        return self.take_turns(30000000)

    def test_cases(self, input_data: str) -> int:
        part1_test = '0,3,6'
        self.common(part1_test)
        assert self.part1(part1_test) == 436
        assert self.part2(part1_test) == 175594

        part1_test = '1,3,2'
        self.common(part1_test)
        assert self.part1(part1_test) == 1
        assert self.part2(part1_test) == 2578

        part1_test = '2,1,3'
        self.common(part1_test)
        assert self.part1(part1_test) == 10
        assert self.part2(part1_test) == 3544142

        part1_test = '1,2,3'
        self.common(part1_test)
        assert self.part1(part1_test) == 27
        assert self.part2(part1_test) == 261214

        part1_test = '2,3,1'
        self.common(part1_test)
        assert self.part1(part1_test) == 78
        assert self.part2(part1_test) == 6895259

        part1_test = '3,2,1'
        self.common(part1_test)
        assert self.part1(part1_test) == 438
        assert self.part2(part1_test) == 18

        part1_test = '3,1,2'
        self.common(part1_test)
        assert self.part1(part1_test) == 1836
        assert self.part2(part1_test) == 362

        self.common(input_data)
        assert self.part1(input_data) == 1522
        assert self.part2(input_data) == 18234

        return 8
