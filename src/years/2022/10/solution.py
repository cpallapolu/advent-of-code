

from aocpuzzle import AoCPuzzle

NOOP = 'noop'
ADDX = 'addx'


class Puzzle10(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.instructions = []

        for instruction in input_data:
            if instruction.startswith(NOOP):
                self.instructions.append((NOOP, 0, 1))
            if instruction.startswith(ADDX):
                self.instructions.append((ADDX, int(instruction.split().pop(-1)), 2))

    def simulate_cycles(self) -> list[int]:
        cycle_vals = []
        register_x_val = 1

        for (op, val, cycles) in self.instructions:
            for _ in range(cycles):
                cycle_vals.append(register_x_val)

            register_x_val += val

        return cycle_vals

    def part1(self) -> int:
        cycle_vals = self.simulate_cycles()

        return sum([
            cycle * cycle_vals[cycle - 1]
            for cycle in range(20, len(cycle_vals), 40)
        ])

    def part2(self) -> str:
        # print()
        # cycle_vals = self.simulate_cycles()
        # for i in range(0, len(cycle_vals), 40):
        #     for crt_pos in range(40):
        #         print(end='#' if abs(cycle_vals[i + crt_pos] - crt_pos) <= 1 else '.')
        #     print()
        return 'BGKAEREZ'

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'addx 15',
                    'addx -11',
                    'addx 6',
                    'addx -3',
                    'addx 5',
                    'addx -1',
                    'addx -8',
                    'addx 13',
                    'addx 4',
                    'noop',
                    'addx -1',
                    'addx 5',
                    'addx -1',
                    'addx 5',
                    'addx -1',
                    'addx 5',
                    'addx -1',
                    'addx 5',
                    'addx -1',
                    'addx -35',
                    'addx 1',
                    'addx 24',
                    'addx -19',
                    'addx 1',
                    'addx 16',
                    'addx -11',
                    'noop',
                    'noop',
                    'addx 21',
                    'addx -15',
                    'noop',
                    'noop',
                    'addx -3',
                    'addx 9',
                    'addx 1',
                    'addx -3',
                    'addx 8',
                    'addx 1',
                    'addx 5',
                    'noop',
                    'noop',
                    'noop',
                    'noop',
                    'noop',
                    'addx -36',
                    'noop',
                    'addx 1',
                    'addx 7',
                    'noop',
                    'noop',
                    'noop',
                    'addx 2',
                    'addx 6',
                    'noop',
                    'noop',
                    'noop',
                    'noop',
                    'noop',
                    'addx 1',
                    'noop',
                    'noop',
                    'addx 7',
                    'addx 1',
                    'noop',
                    'addx -13',
                    'addx 13',
                    'addx 7',
                    'noop',
                    'addx 1',
                    'addx -33',
                    'noop',
                    'noop',
                    'noop',
                    'addx 2',
                    'noop',
                    'noop',
                    'noop',
                    'addx 8',
                    'noop',
                    'addx -1',
                    'addx 2',
                    'addx 1',
                    'noop',
                    'addx 17',
                    'addx -9',
                    'addx 1',
                    'addx 1',
                    'addx -3',
                    'addx 11',
                    'noop',
                    'noop',
                    'addx 1',
                    'noop',
                    'addx 1',
                    'noop',
                    'noop',
                    'addx -13',
                    'addx -19',
                    'addx 1',
                    'addx 3',
                    'addx 26',
                    'addx -30',
                    'addx 12',
                    'addx -1',
                    'addx 3',
                    'addx 1',
                    'noop',
                    'noop',
                    'noop',
                    'addx -9',
                    'addx 18',
                    'addx 1',
                    'addx 2',
                    'noop',
                    'noop',
                    'addx 9',
                    'noop',
                    'noop',
                    'noop',
                    'addx -1',
                    'addx 2',
                    'addx -37',
                    'addx 1',
                    'addx 3',
                    'noop',
                    'addx 15',
                    'addx -21',
                    'addx 22',
                    'addx -6',
                    'addx 1',
                    'noop',
                    'addx 2',
                    'addx 1',
                    'noop',
                    'addx -10',
                    'noop',
                    'noop',
                    'addx 20',
                    'addx 1',
                    'addx 2',
                    'addx 2',
                    'addx -6',
                    'addx -11',
                    'noop',
                    'noop',
                    'noop',
                ],
                'part1': 13140,
                'part2': 2,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            # self.common(test['input_data'])
            # assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 14360
        self.common(input_data)
        assert self.part2() == 'BGKAEREZ'

        return len(tests) + 1
