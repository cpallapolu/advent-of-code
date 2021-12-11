

from aocpuzzle import AoCPuzzle


class Puzzle10(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.bracket_pairs = {
            '(': ')',
            '[': ']',
            '<': '>',
            '{': '}',
        }
        self.mismatch_weights = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137,
        }
        self.closing_weights = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4,
        }
        self.navigation_subsystem = input_data

    def get_mismatches(self, navigation: str) -> list[str]:
        open_brackets = []

        for idx, bracket in enumerate(navigation):
            if bracket in self.bracket_pairs.keys():
                open_brackets.append(idx)

            if bracket in self.bracket_pairs.values():
                closing_bracket = navigation[open_brackets.pop()]

                if self.bracket_pairs[closing_bracket] != bracket:
                    return [bracket]

        return [
            self.bracket_pairs[navigation[idx]]
            for idx in reversed(open_brackets)
        ]

    def part1(self) -> int:
        mismatch_score = 0

        for navigation in self.navigation_subsystem:
            mismatches = self.get_mismatches(navigation)
            if len(mismatches) == 1:
                mismatch_score += self.mismatch_weights[mismatches[0]]

        return mismatch_score

    def part2(self) -> int:
        scores = []

        for navigation in self.navigation_subsystem:
            mismatches = self.get_mismatches(navigation)

            if len(mismatches) == 1:
                continue

            mismatch_score = 0

            for bracket in mismatches:
                mismatch_score *= 5
                mismatch_score += self.closing_weights[bracket]

            scores.append(mismatch_score)

        return sorted(scores)[len(scores) // 2]

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '[({(<(())[]>[[{[]{<()<>>',
                    '[(()[<>])]({[<{<<[]>>(',
                    '{([(<{}[<>[]}>{[]{[(<()>',
                    '(((({<>}<{<{<>}{[]{[]{}',
                    '[[<[([]))<([[{}[[()]]]',
                    '[{[{({}]{}}([{[{{{}}([]',
                    '{<[[]]>}<{[{[{[]{()[[[]',
                    '[<(<(<(<{}))><([]([]()',
                    '<{([([[(<>()){}]>(<<{{',
                    '<{([{{}}[<[[[<>{}]]]>[]]',
                ],
                'part1': 26397,
                'part2': 288957,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 271245
        self.common(input_data)
        assert self.part2() == 1685293086
        return len(tests) + 1
