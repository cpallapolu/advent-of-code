
from itertools import zip_longest
from re import findall

from aocpuzzle import AoCPuzzle


class Puzzle05(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        blank_idx = input_data.index('')
        crates, moves = input_data[:blank_idx], input_data[blank_idx + 1:]

        crate_numbers, crate_contents = crates[::-1][0], crates[::-1][1:]
        crates = [crate[1::4] for crate in [' ' + crate_numbers + ' '] + crate_contents]

        self.crates = {
            int(crate_num): [entry for entry in entries if not entry.isspace()]
            for (crate_num, *entries) in list(zip_longest(*crates, fillvalue=' '))
        }

        self.moves = [
            list(map(int, findall(r'move (\d+) from (\d+) to (\d+)', move).pop()))
            for move in moves
        ]

    def move_crates(self, crate_mover_9000: bool) -> str:
        for qty, src, dest in self.moves:
            to_be_moved = self.crates[src][(-1 * qty):]

            if crate_mover_9000:
                to_be_moved.reverse()

            self.crates[dest] += to_be_moved
            self.crates[src] = self.crates[src][:len(self.crates[src]) - qty]

        return ''.join([crate[-1] for crate in self.crates.values()])

    def part1(self) -> str:
        return self.move_crates(True)

    def part2(self) -> str:
        return self.move_crates(False)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '    [D]    ',
                    '[N] [C]    ',
                    '[Z] [M] [P]',
                    '1   2   3',
                    '',
                    'move 1 from 2 to 1',
                    'move 3 from 1 to 3',
                    'move 2 from 2 to 1',
                    'move 1 from 1 to 2',
                ],
                'part1': 'CMZ',
                'part2': 'MCD',
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 'RNZLFZSJH'
        self.common(input_data)
        assert self.part2() == 'CNSFCGJSM'

        return len(tests) + 1
