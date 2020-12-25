from collections import defaultdict
from math import prod
from typing import Dict, List

from aocpuzzle import AoCPuzzle


class Puzzle16(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.notes: Dict[str, List[int]] = defaultdict(list)
        self.your_ticket: List[int] = []
        self.nearby_tickets = []

        notes, my_ticket, nearby_tickets = '\n'.join(input_data).split('\n\n')

        for note in notes.split('\n'):
            name, ranges = note.split(': ')
            values = ranges.split(' or ')

            for value in values:
                low, high = value.split('-')
                for num in range(int(low), int(high) + 1):
                    self.notes[name].append(num)

        self.my_ticket = list(map(int, my_ticket.split('\n')[1].split(',')))

        self.nearby_tickets = [
            list(map(int, nearby_ticket.split(',')))
            for nearby_ticket in nearby_tickets.split('\n')[1:]
        ]

    def check_rule(self, note_values: List[int], number: int) -> bool:
        return number in note_values

    def check_rules(self, number: int) -> bool:
        for note in self.notes.values():
            if self.check_rule(note, number):
                return True
        return False

    def part1(self) -> int:
        error_rate = 0

        for nearby_ticket in self.nearby_tickets:
            for ticket_val in nearby_ticket:
                if self.check_rules(ticket_val) is False:
                    error_rate += ticket_val
        return error_rate

    def validate_ticket(self, ticket: list) -> bool:
        for number in ticket:
            if self.check_rules(number) is False:
                return False
        return True

    def get_valid_tickets(self) -> List[List[int]]:
        valid_tickets = []

        for nearby_ticket in self.nearby_tickets:
            if self.validate_ticket(nearby_ticket) is True:
                valid_tickets.append(nearby_ticket)
        return valid_tickets

    def get_possible_field_options(self) -> Dict[str, List[int]]:
        possible_field_options = defaultdict(list)

        for name, note_values in self.notes.items():
            positions = []

            for idx in range(len(self.my_ticket)):
                idx_valid = all(
                    [
                        self.check_rule(note_values, valid_ticket[idx])
                        for valid_ticket in self.valid_tickets
                    ],
                )
                if idx_valid is True:
                    positions.append(idx)
            possible_field_options[name] = positions

        return possible_field_options

    def find_positions(self) -> Dict[str, int]:
        positions = defaultdict(int)

        fields = list(self.field_options.keys())

        while len(fields) > 0:
            for field in fields:
                if len(self.field_options[field]) == 1:
                    positions[field] = self.field_options[field][0]
                    fields.remove(field)

                    for f in fields:
                        if positions[field] in self.field_options[f]:
                            self.field_options[f].remove(positions[field])
                    continue

        return positions

    def part2(self) -> int:
        self.valid_tickets = self.get_valid_tickets()
        self.field_options = self.get_possible_field_options()
        self.field_map = self.find_positions()

        res = prod(
            self.my_ticket[val]
            for field, val in self.field_map.items()
            if field.startswith('departure')
        )

        return res

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            'class: 1-3 or 5-7',
            'row: 6-11 or 33-44',
            'seat: 13-40 or 45-50',
            '',
            'your ticket:',
            '7,1,14',
            '',
            'nearby tickets:',
            '7,3,47',
            '40,4,50',
            '55,2,20',
            '38,6,12',
        ]
        self.common(tests)
        assert self.part1() == 71

        tests = [
            'class: 0-1 or 4-19',
            'row: 0-5 or 8-19',
            'seat: 0-13 or 16-19',
            '',
            'your ticket:',
            '11,12,13',
            '',
            'nearby tickets:',
            '3,9,18',
            '15,1,5',
            '5,14,9',
        ]
        self.common(tests)
        assert self.part2() == 1

        self.common(input_data)
        assert self.part1() == 19060
        self.common(input_data)
        assert self.part2() == 953713095011

        return 3
