

from aocpuzzle import AoCPuzzle

SCORE_ROCK = 1
SCORE_PAPER = 2
SCORE_SCISSORS = 3
SCORE_LOST = 0
SCORE_DRAW = 3
SCORE_WIN = 6
ROCK_OPTIONS = ['A', 'X']
PAPER_OPTIONS = ['B', 'Y']
SCISSORS_OPTIONS = ['C', 'Z']


class Puzzle02(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.rounds = []

        for data in input_data:
            opponent, you = data.split()
            self.rounds.append(((ord(opponent) - ord('A'), ord(you) - ord('X'))))

    def score(self, opponent: int, you: int) -> int:
        if (opponent - 1) % 3 == you:
            return you + SCORE_LOST + 1
        if (you - 1) % 3 == opponent:
            return you + SCORE_WIN + 1
        return you + SCORE_DRAW + 1

    def part1(self) -> int:
        return sum(self.score(opponent, you) for (opponent, you) in self.rounds)

    def part2(self) -> int:
        self.new_rounds = [
            (opponent, (opponent + you - 1) % 3)
            for (opponent, you) in self.rounds
        ]
        return sum(self.score(opponent, you) for (opponent, you) in self.new_rounds)

    def test_cases(self, input_data: list[str]) -> int:
        print('day02 test_cases in day02')
        tests: list[dict] = [
            {
                'input_data': [
                    'A Y',
                    'B X',
                    'C Z',
                ],
                'part1': 15,
                'part2': 12,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 10816
        self.common(input_data)
        assert self.part2() == 11657

        return len(tests) + 1
