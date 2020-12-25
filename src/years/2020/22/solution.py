from collections import defaultdict
from typing import Dict, List, Tuple, Union

from aocpuzzle import AoCPuzzle

Decks = Dict[str, List[int]]


class Puzzle22(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.decks = defaultdict(list)
        input_data = '\n'.join(input_data).split('\n\n')

        for player in input_data:
            lines = player.split('\n')
            player_name = lines.pop(0).replace(':', '')
            decks = list(map(int, lines))
            self.decks[player_name] = decks

    def total_cards(self, decks: Decks) -> int:
        return sum(len(x) for x in decks.values())

    def play_rounds_part1(self) -> Union[str, None]:
        top_cards = [(d[0], d[1].pop(0)) for d in self.decks.items()]

        top_player, _ = max(top_cards, key=lambda tc: tc[1])

        self.decks[top_player].extend(sorted([tc[1] for tc in top_cards], reverse=True))

        return top_player if len(self.decks[top_player]) == self.total_cards(self.decks) else None

    def get_score(self, decks: List[int]) -> int:
        multiplier = 1
        result = 0

        for card in decks[::-1]:
            result += card * multiplier
            multiplier += 1
        return result

    def part1(self) -> int:
        winner = None

        while winner is None:
            winner = self.play_rounds_part1()

        return self.get_score(self.decks[winner])

    def play_rounds_part2(self, decks: Decks) -> Tuple[Union[str, None], Decks]:
        top_cards = [(d[0], d[1].pop(0)) for d in decks.items()]

        if all(len(decks[tc[0]]) >= tc[1] for tc in top_cards):
            top_player = self.play_subgame(decks, top_cards)
            top_cards_dict = dict(top_cards)
            decks[top_player].append(top_cards_dict[top_player])
            top_cards_dict.pop(top_player)

            decks[top_player].append(list(top_cards_dict.values())[0])

        else:
            top_player, _ = max(top_cards, key=lambda tc: tc[1])
            decks[top_player].extend(sorted([tc[1] for tc in top_cards], reverse=True))

        if len(decks[top_player]) == self.total_cards(decks):
            return top_player, decks
        else:
            return None, decks

    def get_winner_part2(self, decks: Decks) -> str:
        winner = None
        round_states: Dict = defaultdict(bool)

        while winner is None:
            state_key = tuple(tuple(c[1]) for c in decks.items())
            if round_states[state_key] is True:
                return 'Player 1'

            round_states[state_key] = True

            winner, decks = self.play_rounds_part2(decks)
        return winner

    def play_subgame(self, decks: Decks, top_cards: List[Tuple[str, int]]) -> str:
        decks = {tc_p: decks[tc_p][:tc_c] for tc_p, tc_c in top_cards}

        return self.get_winner_part2(decks)

    def part2(self) -> int:
        winner = self.get_winner_part2(self.decks)

        return self.get_score(self.decks[winner])

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            'Player 1:',
            '9',
            '2',
            '6',
            '3',
            '1',
            '',
            'Player 2:',
            '5',
            '8',
            '4',
            '7',
            '10',
        ]
        self.common(tests)
        assert self.part1() == 306
        self.common(tests)
        assert self.part2() == 291

        self.common(input_data)
        assert self.part1() == 33561
        self.common(input_data)
        assert self.part2() == 34594

        return 2
