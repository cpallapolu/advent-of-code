
from heapq import heappop, heappush

from aocpuzzle import AoCPuzzle


class Puzzle15(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.input_data = input_data

    def build_map(self, times: int) -> None:
        self.risk_map: dict[tuple[int, int], int] = {
            (x, y): int(risk)
            for x, row in enumerate(self.input_data * times)
            for y, risk in enumerate(row * times)
        }

        initial_rows, initial_cols = len(self.input_data), len(self.input_data[0])

        self.last_row = ((len(self.input_data)) * times) - 1
        self.last_col = ((len(self.input_data[0])) * times) - 1

        if times == 5:
            for new_row in range(self.last_row + 1):
                for new_col in range(self.last_col + 1):
                    self.risk_map[(new_row, new_col)] = 1 + (
                        self.risk_map[(new_row, new_col)]
                        + (new_row // initial_rows)
                        + ((new_col // initial_cols) - 1)
                    ) % 9

    def get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        neighbors = []

        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + x, col + y

            if (new_row, new_col) in self.risk_map:
                neighbors.append((new_row, new_col))

        return neighbors

    def path(self) -> int:
        pq = [(0, (0, 0))]
        visited = set({(0, 0)})

        while len(pq) > 0:
            curr_risk, (row, col) = heappop(pq)

            if row == self.last_row and col == self.last_col:
                return curr_risk

            for neighbor_row, neighbor_col in self.get_neighbors(row, col):
                if (neighbor_row, neighbor_col) not in visited:
                    new_risk = curr_risk + self.risk_map[(neighbor_row, neighbor_col)]
                    heappush(
                        pq,
                        (new_risk, (neighbor_row, neighbor_col)),
                    )
                    visited.add((neighbor_row, neighbor_col))
        return 0

    def part1(self) -> int:
        self.build_map(1)
        return self.path()

    def part2(self) -> int:
        self.build_map(5)

        return self.path()

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '1163751742',
                    '1381373672',
                    '2136511328',
                    '3694931569',
                    '7463417111',
                    '1319128137',
                    '1359912421',
                    '3125421639',
                    '1293138521',
                    '2311944581',
                ],
                'part1': 40,
                'part2': 315,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 621
        self.common(input_data)
        assert self.part2() == 2904

        return len(tests) + 1
