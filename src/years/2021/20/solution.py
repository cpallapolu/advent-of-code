
from itertools import product

from aocpuzzle import AoCPuzzle

CoordType = tuple[int, int]


class Puzzle20(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.enhancement = {
            idx: char
            for idx, char in enumerate(input_data[0])
        }

        self.image: set[CoordType] = set(
            (row, col)
            for row, line in enumerate(input_data[2:])
            for col, char in enumerate(line)
            if char == '#'
        )

    def update_boundaries(self) -> None:
        x_values = set([x for x, _ in self.image])
        y_values = set([y for _, y in self.image])

        self.min_x = min(x_values) - 1
        self.max_x = max(x_values) + 2
        self.min_y = min(y_values) - 1
        self.max_y = max(y_values) + 2

    def get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        return [(row + x, col + y) for x, y in product([-1, 0, 1], repeat=2)]

    def enhance(self, steps: int) -> None:
        for step in range(1, steps + 1):
            new_image = set()
            self.update_boundaries()

            default = '.' if step % 2 == 1 else '#'

            for row in range(self.min_x, self.max_x):
                for col in range(self.min_y, self.max_y):
                    bits = ''
                    for neighbor_row, neighbor_col in self.get_neighbors(row, col):
                        if step % 2 == 1:
                            bits += '1' if (neighbor_row, neighbor_col) in self.image else '0'
                        else:
                            bits += '1' if (neighbor_row, neighbor_col) not in self.image else '0'

                    if self.enhancement[int(bits, 2)] == default:
                        new_image.add((row, col))

            self.image = new_image

    def part1(self) -> int:
        self.enhance(2)

        return len(self.image)

    def part2(self) -> int:
        self.enhance(50)

        return len(self.image)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    ''.join([
                        '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#.',
                        '.#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..',
                        '#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....',
                        '#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####',
                        '.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.',
                        '#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..',
                        '#.##.#....##..#.####....##...##..#...#......#.#.......#.......##',
                        '..####..#...#.#.#...##..#.#..###..#####........#..####......#..#',
                    ]),
                    '',
                    '#..#.',
                    '#....',
                    '##..#',
                    '..#..',
                    '..###',
                ],
                'part1': 31,
                'part2': 5132,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 5846
        self.common(input_data)
        assert self.part2() == 21149

        return len(tests) + 1
