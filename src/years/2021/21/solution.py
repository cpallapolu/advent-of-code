
from collections import Counter
from functools import lru_cache
from itertools import product

from aocpuzzle import AoCPuzzle


class Player:
    def __init__(self, position: int) -> None:
        self.position = position
        self.score = 0

    def take_turn(self, roll_sum: int) -> None:
        self.position = (self.position + roll_sum) % 10

        self.score += self.position + 1


class Game:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.num_players = len(players)
        self.curr_player_idx = 0
        self.die = 1
        self.num_rolls = 0

    def roll_die(self, times: int) -> int:
        roll_sum = 0

        for _ in range(times):
            roll_sum += self.die
            self.die = self.die % 100 + 1

        self.num_rolls += times

        return roll_sum

    def roll_quantum_die(self) -> None:
        self.quantum_rolls = Counter(
            sum(roll)
            for roll in product([1, 2, 3], repeat=3)
        )

    def next_turn(self) -> bool:
        curr_player = self.players[self.curr_player_idx]

        curr_player.take_turn(self.roll_die(3))

        if curr_player.score >= 1000:
            self.loser = self.players[1 if self.curr_player_idx == 0 else 0]

            return True

        self.curr_player_idx = (self.curr_player_idx + 1) % self.num_players

        return False

    def play(self) -> None:
        got_winner = self.next_turn()

        while got_winner is False:
            got_winner = self.next_turn()

    def play_qunatum(self) -> None:
        self.roll_quantum_die()

        (
            self.player_1_universes,
            self.player_2_universes,
        ) = self.play_quantum_helper(self.players[0].position, self.players[1].position, 0, 0)

    @lru_cache(maxsize=None)
    def play_quantum_helper(
        self,
        player_1_pos: int,
        player_2_pos: int,
        player_1_score: int,
        player_2_score: int,
    ) -> tuple[int, int]:
        if player_2_score >= 21:
            return (player_1_score >= 21, player_2_score >= 21)

        player_1_universes, player_2_universes = 0, 0

        for roll, freq in self.quantum_rolls.items():
            new_position = (player_1_pos + roll) % 10
            new_score = player_1_score + new_position + 1

            (
                new_player_2_score,
                new_player_1_score,
            ) = self.play_quantum_helper(player_2_pos, new_position, player_2_score, new_score)

            player_1_universes = player_1_universes + (new_player_1_score * freq)
            player_2_universes = player_2_universes + (new_player_2_score * freq)

        return (player_1_universes, player_2_universes)


class Puzzle21(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.players = [
            Player(int(line[-1]) - 1)
            for line in input_data
        ]

    def part1(self) -> int:
        game = Game(self.players)

        game.play()

        return game.num_rolls * game.loser.score

    def part2(self) -> int:
        game = Game(self.players)

        game.play_qunatum()

        return max(game.player_1_universes, game.player_2_universes)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'Player 1 starting position: 4',
                    'Player 2 starting position: 8',
                ],
                'part1': 739785,
                'part2': 444356092776315,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        return len(tests) + 1
