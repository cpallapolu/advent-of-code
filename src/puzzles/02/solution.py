from collections import Counter
from typing import Dict, List

from aocpuzzle import AoCPuzzle


class PasswordRuleLen:
    def __init__(self, min_len: int, max_len: int, char: str, password: str) -> None:
        self.min_len = min_len
        self.max_len = max_len
        self.char = char
        self.password = password


class PasswordRulePos:
    def __init__(self, pos1: int, pos2: int, char: str, password: str) -> None:
        self.pos1 = pos1
        self.pos2 = pos2
        self.char = char
        self.password = password


class Puzzle02(AoCPuzzle):
    def process_part1_input_data(self, input_data: List[str]) -> List[PasswordRuleLen]:
        processed_input_data = []

        for rule in input_data:
            [min_len, rest] = rule.split('-')
            [max_char_len, password] = rest.split(':')
            [max_len, char] = max_char_len.split(' ')
            password_rule_len = PasswordRuleLen(
                int(min_len.strip()),
                int(max_len.strip()),
                char.strip(),
                password.strip(),
            )
            processed_input_data.append(password_rule_len)

        return processed_input_data

    def process_part2_input_data(self, input_data: List[str]) -> List[PasswordRulePos]:
        processed_input_data = []

        for rule in input_data:
            [pos1, rest] = rule.split('-')
            [pos2_char_len, password] = rest.split(':')
            [pos2, char] = pos2_char_len.split(' ')
            password_rule_pos = PasswordRulePos(
                int(pos1.strip()),
                int(pos2.strip()),
                char.strip(),
                password.strip(),
            )
            processed_input_data.append(password_rule_pos)

        return processed_input_data

    def part1(self, input_data: List[str]) -> int:
        valid_passwords = 0

        for data in self.process_part1_input_data(input_data):
            password_counter: Dict[str, int] = Counter(data.password)

            if data.min_len <= password_counter[data.char] <= data.max_len:
                valid_passwords += 1

        return valid_passwords

    def part2(self, input_data: List[str]) -> int:
        valid_passwords = 0

        for data in self.process_part2_input_data(input_data):
            char_pos1 = data.password[data.pos1 - 1]
            char_pos2 = data.password[data.pos2 - 1]

            char_only_pos1 = data.char == char_pos1 and data.char != char_pos2
            char_only_pos2 = data.char != char_pos1 and data.char == char_pos2

            if char_only_pos1 or char_only_pos2:
                valid_passwords += 1
        return valid_passwords

    def test_cases(self, input_data: List[str]) -> int:
        tests = ['1-3 a: abcde', '1-3 b: cdefg', '2-9 c: ccccccccc']

        assert self.part1(tests) == 2
        assert self.part2(tests) == 1

        return 6
