
from aocpuzzle import AoCPuzzle


class Puzzle01(AoCPuzzle):
    def __calculate_increases(self, depths: list[int]) -> int:
        increases = 0
        prev_depth = depths[0]

        for depth in depths:
            increases += 1 if depth > prev_depth else 0
            prev_depth = depth

        return increases

    def __get_windows_sum(self) -> list[int]:
        return [
            sum(self.depths[idx:idx + 3])
            for idx in range(len(self.depths) - 2)
        ]

    def common(self, input_data: list[str]) -> None:
        self.depths = list(map(int, input_data))

    def part1(self) -> int:
        return self.__calculate_increases(self.depths)

    def part2(self) -> int:
        return self.__calculate_increases(self.__get_windows_sum())

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '199', '200', '208', '210', '200',
                    '207', '240', '269', '260', '263',
                ],
                'part1': 7,
                'part2': 5,
            },
        ]

        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 1709
        self.common(input_data)
        assert self.part2() == 1761

        return len(tests) + 1
