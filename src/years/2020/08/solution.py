from typing import Any, List, Tuple

from aocpuzzle import AoCPuzzle


class Instruction:
    def __init__(self, op: str, arg: int) -> None:
        self.op = op
        self.arg = arg
        self.executed = False


class Puzzle08(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.instructions = []

        for idx, instruction in enumerate(input_data):
            op, arg = instruction.split(' ')
            self.instructions.append(Instruction(op, int(arg)))

    def execute_instructions(self) -> Tuple[int, bool]:
        idx = 0
        accumulator = 0

        while True:
            if idx == len(self.instructions):
                return (accumulator, True)

            instruction = self.instructions[idx]

            if instruction.executed is True:
                return (accumulator, False)

            if instruction.op == 'acc':
                accumulator += instruction.arg

            idx += 1 if instruction.op in ['nop', 'acc'] else instruction.arg

            instruction.executed = True

    def part1(self, input_data: List[str]) -> int:
        return self.execute_instructions()[0]

    def part2(self, input_data: List[str]) -> int:
        for instruction in self.instructions:
            if instruction.op == 'acc':
                continue

            original_op = (instruction.op)
            instruction.op = 'nop' if instruction.op == 'jmp' else 'jmp'

            accumulator, complete = self.execute_instructions()

            if complete is True:
                return accumulator

            instruction.op = original_op

            for instruction in self.instructions:
                instruction.executed = False

        return 0

    def test_cases(self, input_data: Any) -> int:
        part1_tests = [
            'nop +0',
            'acc +1',
            'jmp +4',
            'acc +3',
            'jmp -3',
            'acc -99',
            'acc +1',
            'jmp -4',
            'acc +6',
        ]
        self.common(part1_tests)
        assert self.part1(part1_tests) == 5
        assert self.part2(part1_tests) == 8

        self.common(input_data)
        assert self.part1(input_data) == 1684
        assert self.part2(input_data) == 2188

        return 2
