from collections import defaultdict
from typing import Dict, List

from aocpuzzle import AoCPuzzle

MASK = 'mask'
MEM = 'mem'


class Instruction:
    def __init__(self) -> None:
        self.mask = ''
        self.mask_0 = 0
        self.mask_1 = 1
        self.mems: List[List[int]] = []


class Puzzle14(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.instructions = []
        self.mem: Dict[int, int] = defaultdict(int)

        for line in '\n'.join(input_data).replace('mask', '\nmask')[1:].split('\n\n'):
            [mask, *mems] = line.split('\n')

            instruction = Instruction()

            mask_val = mask.split(' = ')[1]

            instruction.mask = mask_val
            instruction.mask_0 = int(mask_val.replace('X', '0'), base=2)
            instruction.mask_1 = int(mask_val.replace('X', '1'), base=2)

            for mem in mems:
                loc, val = mem.split(' = ')
                instruction.mems.append([int(loc[4:-1]), int(val)])

            self.instructions.append(instruction)

    def part1(self, input_data: List[str]) -> int:
        for instruction in self.instructions:
            for loc, val in instruction.mems:
                self.mem[loc] = val & instruction.mask_1 | instruction.mask_0

        return sum(self.mem.values())

    def floating(self, mask: str) -> List[str]:
        if 'X' in mask:
            mask_0, mask_1 = mask.replace('X', '0', 1), mask.replace('X', '1', 1)

            masks = self.floating(mask_0)
            masks += self.floating(mask_1)

            return masks if masks != [] else [mask_0, mask_1]

        return []

    def part2(self, input_data: List[str]) -> int:
        for instruction in self.instructions:
            for loc, val in instruction.mems:
                loc = loc | instruction.mask_0

                loc_mask = f'{loc:036b}'

                for idx, bit in enumerate(instruction.mask):
                    if bit == 'X':
                        loc_mask = loc_mask[:idx] + 'X' + loc_mask[idx + 1:]

                floating_locs = self.floating(loc_mask)

                for floating_loc in floating_locs:
                    self.mem[int(floating_loc, base=2)] = val

        return sum(self.mem.values())

    def test_cases(self, input_data: List[str]) -> int:
        part1_tests = [
            'mask = 000000000000000000000000000000X1XXXX0X',
            'mem[8] = 11',
            'mem[7] = 101',
            'mem[8] = 0',
        ]

        self.common(part1_tests)
        assert self.part1(part1_tests) == 165
        self.common(part1_tests)
        assert self.part2(part1_tests) == 0

        part2_tests = [
            'mask = 000000000000000000000000000000X1001X',
            'mem[42] = 100',
            'mask = 00000000000000000000000000000000X0XX',
            'mem[26] = 1',
        ]
        self.common(part2_tests)
        assert self.part1(part2_tests) == 51
        self.common(part2_tests)
        assert self.part2(part2_tests) == 208

        self.common(input_data)
        assert self.part1(input_data) == 13105044880745

        self.common(input_data)
        assert self.part2(input_data) == 3505392154485

        return 3
