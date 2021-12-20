
from collections import defaultdict

from aocpuzzle import AoCPuzzle


class Puzzle14(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.polymer = input_data[0]
        self.pairs: dict[str, int] = defaultdict(lambda: 0)

        for idx, element in enumerate(self.polymer[:-1]):
            self.pairs[f'{element}{self.polymer[idx + 1]}'] += 1

        self.insertion_pairs = defaultdict(str)

        for insertion_pair in input_data[2:]:
            element_pair, insertion_element = insertion_pair.split(' -> ')
            self.insertion_pairs[element_pair] = insertion_element

    def step(self) -> None:
        new_pairs: dict[str, int] = defaultdict(lambda: 0)

        for pair in self.pairs:
            element_one, element_two = list(pair)

            to_insert_element = self.insertion_pairs[pair]

            first_new = f'{element_one}{to_insert_element}'
            second_new = f'{to_insert_element}{element_two}'

            new_pairs[first_new] += self.pairs[pair]
            new_pairs[second_new] += self.pairs[pair]

        self.pairs = new_pairs

    def get_diff(self) -> int:
        elements_count: dict[str, int] = defaultdict(lambda: 0)

        for pair, count in self.pairs.items():
            elements_count[pair[0]] += count

        elements_count[self.polymer[-1]] += 1

        return max(elements_count.values()) - min(elements_count.values())

    def part1(self) -> int:
        for _ in range(10):
            self.step()

        return self.get_diff()

    def part2(self) -> int:
        for _ in range(40):
            self.step()

        return self.get_diff()

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'NNCB',
                    '.',
                    'CH -> B',
                    'HH -> N',
                    'CB -> H',
                    'NH -> C',
                    'HB -> C',
                    'HC -> B',
                    'HN -> C',
                    'NN -> C',
                    'BH -> H',
                    'NC -> B',
                    'NB -> B',
                    'BN -> B',
                    'BB -> N',
                    'BC -> B',
                    'CC -> N',
                    'CN -> C',
                ],
                'part1': 1588,
                'part2': 2188189693529,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 2345
        self.common(input_data)
        assert self.part2() == 2432786807053

        return len(tests) + 1
