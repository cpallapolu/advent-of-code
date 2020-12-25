
from typing import Dict, List

from aocpuzzle import AoCPuzzle


class Cup:
    def __init__(self, label: int, next_cup=None) -> None:
        self.label = label
        self.next = next_cup


class Puzzle23(AoCPuzzle):
    def common(self, input_data: str) -> None:
        self.cups = list(map(int, list(input_data)))
        self.cups_dict: Dict[int, Cup] = {}

    def pick_cups(self) -> List[int]:
        picked_cups = [self.cups.pop(0) for i in range(3)]

        return picked_cups

    def destination_cup(self, destination: int, picked_cups: List[int]) -> int:
        if destination == 0:
            destination = max(self.cups)

        while destination in picked_cups:
            destination -= 1

            if destination == 0:
                destination = max(self.cups)

        return destination

    def play_game(self, cups_len: int, moves: int) -> None:
        curr_cup = self.cups_dict[self.cups[0]]

        for idx in range(moves):
            first = curr_cup.next
            second = first.next
            third = second.next

            curr_cup.next = third.next

            picked_cups = [curr_cup.label, first.label, second.label, third.label]
            curr_label = curr_cup.label
            while curr_label in picked_cups:
                curr_label = curr_label - 1 if curr_label != 1 else cups_len

            destination = self.cups_dict[curr_label]
            next_node = destination.next

            destination.next = first
            third.next = next_node

            curr_cup = curr_cup.next

    def part1(self) -> str:
        for label in range(1, len(self.cups) + 1):
            self.cups_dict[label] = Cup(label)

        for i in range(len(self.cups)):
            self.cups_dict[self.cups[i]].next = self.cups_dict[self.cups[(i + 1) % len(self.cups)]]

        self.play_game(len(self.cups), 100)
        pointer, ans = self.cups_dict[1], ''

        for _ in range(len(self.cups) - 1):
            pointer = pointer.next
            ans += str(pointer.label)

        return ans

    def part2(self) -> int:
        for idx in range(max(self.cups) + 1, 1000001):
            self.cups.append(idx)

        for label in range(1, len(self.cups) + 1):
            self.cups_dict[label] = Cup(label)

        for i in range(len(self.cups)):
            self.cups_dict[self.cups[i]].next = self.cups_dict[self.cups[(i + 1) % len(self.cups)]]

        self.play_game(len(self.cups), 10000000)

        pointer = self.cups_dict[1]
        first = pointer.next
        second = first.next

        return first.label * second.label

    def test_cases(self, input_data: str) -> int:
        self.common('389125467')
        assert self.part1() == '67384529'
        self.common('389125467')
        assert self.part2() == 149245887792

        self.common(input_data)
        assert self.part1() == '45798623'
        self.common(input_data)
        assert self.part2() == 235551949822

        return 2
