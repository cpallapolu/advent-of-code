
from aocpuzzle import AoCPuzzle

"""
Constraints

Only three parts of input vary - div z, add x, add y for each of the 14 digits.

7 of these blocks have div z as 1 and 7 have div z 26

`div z 1` blocks always have line 8(eql x 0) == 1 as above line(eql x w) is guaranteed to be
false due to (add x value) always being above 9 (the max value that w can be set
to after "inp w".)
When x == 1 after above (guaranteed when div z == 1) y ends up as 26:
    - Set to 0 by mul, + 25, * x then add 1
if x == 0 then x == w (1-9) (mul y x) (line 11) == 0 meaning y == 1
if y == 1 then z - which == z from previous if div z == 1 else a multiple of
26 (or 0 if accumulation hasn't got above 26)
y is then set to w - mul 0 (line 14), y_var added, multiplied by x (0 or 1):
y added to z. Need z == 0 for valid at final block which means y has to be -z
or both are 0 (that possible?)
This means that z, despite accumulation, has to be a one digit integer at this
stage or y couldn't get big enough to zero it out.
Therefore whilst div z 26 can either result in adding or removing a digit -
whereas div z 1 always adds one - in valid inputs it has to remove one to
be a single digit at the end for y to have a chance at negating z

So all instances of div z 26 must meet the criteria of:
    Whatever z is for that block % 26 + what add x is going to be == inp w
inp based on model number and we want highest so 9 down to 1 inclusive

Part Two we want lowest so do 1 up to 9 inclusive instead
"""


class Puzzle24(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.constraints: list[tuple[tuple[int, int], int]] = []
        self.add_x, self.div_z, self.add_y = [], [], []

        for idx, line in enumerate(input_data):
            arr = line.split(' ')

            if arr[0] == 'div' and arr[1] == 'z':
                self.div_z.append(int(arr[2]))
            elif arr[0] == 'add' and arr[1] == 'x' and arr[2].lstrip('-').isdigit() is True:
                self.add_x.append(int(arr[2]))
            elif arr[0] == 'add' and arr[1] == 'y' and arr[2].lstrip('-').isdigit() is True:
                if idx % 9 == 6:
                    self.add_y.append(int(arr[2]))

        self.monad = list(zip(self.div_z, self.add_x, self.add_y))
        self.get_constraints()

    def get_constraints(self) -> None:
        stack = []

        for idx, (divisor, arg1, arg2) in enumerate(self.monad):
            if divisor == 1:
                stack.append((idx, arg2))
            else:
                next_idx, offset = stack.pop()
                self.constraints.append(((next_idx, idx), arg1 + offset))

    def get_model_number(self, part: int) -> int:
        model_number = [0] * 14

        for (idx1, idx2), offset in self.constraints:
            possible_digits = [
                (digit, digit + offset)
                for digit in range(1, 10)
                if 0 < (digit + offset) < 10
            ]

            model_number[idx1], model_number[idx2] = (
                max(possible_digits)
                if part == 1
                else min(possible_digits)
            )

        return int(''.join(str(digit) for digit in model_number))

    def part1(self) -> int:
        return self.get_model_number(1)

    def part2(self) -> int:
        return self.get_model_number(2)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = []

        self.common(input_data)
        assert self.part1() == 93959993429899
        self.common(input_data)
        assert self.part2() == 11815671117121

        return len(tests) + 1
