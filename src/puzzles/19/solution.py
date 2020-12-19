from collections import defaultdict
from re import fullmatch
from typing import List

from aocpuzzle import AoCPuzzle


class Puzzle19(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        raw_rules, messages = '\n'.join(input_data).split('\n\n')
        self.rules = defaultdict(list)
        self.messages = messages.split('\n')

        for rule in raw_rules.split('\n'):
            rule_num, rule_vals = rule.split(': ')

            for rule_val in rule_vals.split(' | '):
                sub_rules = rule_val.split()

                if sub_rules[0] in ['"a"', '"b"']:
                    self.rules[int(rule_num)].append(eval(sub_rules[0]))
                else:
                    self.rules[int(rule_num)].append(list(eval(part)for part in sub_rules))

    def check_message(self, message: str, rule_ids: List[int]) -> bool:
        if len(rule_ids) == 0:
            return len(message) == 0

        rule_id = rule_ids.pop(0)
        sub_rules = self.rules[rule_id]

        if sub_rules[0] in ['a', 'b']:
            return message.startswith(sub_rules[0][0]) and self.check_message(message[1:], rule_ids)
        else:
            return any(
                self.check_message(message, sub_rule + rule_ids)
                for sub_rule in sub_rules
            )

    def part1(self, input_data: List[str]) -> int:
        return sum(self.check_message(message, [0]) for message in self.messages)

    def part2(self, input_data: List[str]) -> int:
        self.rules[8], self.rules[11] = [[42], [42, 8]], [[42, 31], [42, 11, 31]]
        return sum(self.check_message(message, [0]) for message in self.messages)

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            '0: 4 1 5',
            '1: 2 3 | 3 2',
            '2: 4 4 | 5 5',
            '3: 4 5 | 5 4',
            '4: "a"',
            '5: "b"',
            '',
            'ababbb',
            'bababa',
            'abbbab',
            'aaabbb',
            'aaaabbb',
        ]
        self.common(tests)
        assert self.part1(tests) == 2

        self.common(tests)
        assert self.part2(tests) == 2

        tests = [
            '42: 9 14 | 10 1',
            '9: 14 27 | 1 26',
            '10: 23 14 | 28 1',
            '1: "a"',
            '11: 42 31',
            '5: 1 14 | 15 1',
            '19: 14 1 | 14 14',
            '12: 24 14 | 19 1',
            '16: 15 1 | 14 14',
            '31: 14 17 | 1 13',
            '6: 14 14 | 1 14',
            '2: 1 24 | 14 4',
            '0: 8 11',
            '13: 14 3 | 1 12',
            '15: 1 | 14',
            '17: 14 2 | 1 7',
            '23: 25 1 | 22 14',
            '28: 16 1',
            '4: 1 1',
            '20: 14 14 | 1 15',
            '3: 5 14 | 16 1',
            '27: 1 6 | 14 18',
            '14: "b"',
            '21: 14 1 | 1 14',
            '25: 1 1 | 1 14',
            '22: 14 14',
            '8: 42',
            '26: 14 22 | 1 20',
            '18: 15 15',
            '7: 14 5 | 1 21',
            '24: 14 1',
            '',
            'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
            'bbabbbbaabaabba',
            'babbbbaabbbbbabbbbbbaabaaabaaa',
            'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
            'bbbbbbbaaaabbbbaaabbabaaa',
            'bbbababbbbaaaaaaaabbababaaababaabab',
            'ababaaaaaabaaab',
            'ababaaaaabbbaba',
            'baabbaaaabbaaaababbaababb',
            'abbbbabbbbaaaababbbbbbaaaababb',
            'aaaaabbaabaaaaababaa',
            'aaaabbaaaabbaaa',
            'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
            'babaaabbbaaabaababbaabababaaab',
            'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
        ]

        self.common(tests)
        assert self.part1(tests) == 3

        self.common(tests)
        assert self.part2(tests) == 12

        self.common(input_data)
        assert self.part1(tests) == 120

        self.common(input_data)
        assert self.part2(tests) == 350

        return 3
