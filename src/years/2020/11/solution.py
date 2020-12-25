from typing import Callable, List

from aocpuzzle import AoCPuzzle

FLOOR = '.'
EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'


class Puzzle11(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.rows, self.cols = len(input_data), len(input_data[0])
        self.seat_map = [[FLOOR for _ in range(self.cols)] for _ in range(self.rows)]

        for r_idx, row in enumerate(input_data):
            for c_idx, col in enumerate(row):
                if col == OCCUPIED_SEAT:
                    self.seat_map[r_idx][c_idx] = OCCUPIED_SEAT
                elif col == EMPTY_SEAT:
                    self.seat_map[r_idx][c_idx] = EMPTY_SEAT

    def adjacent_seats(self, row: int, col: int) -> List[str]:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        return [
            self.seat_map[row + dx][col + dy]
            for dx, dy in directions
            if 0 <= (row + dx) < self.rows and 0 <= (col + dy) < self.cols
        ]

    def do_round(self, adjacent_seats_func: Callable, occupied_seat_count: int) -> bool:
        changed = False
        new_seat_map = [[FLOOR for _ in range(self.cols)] for _ in range(self.rows)]

        for r_idx, row in enumerate(self.seat_map):
            for c_idx, col in enumerate(row):
                adj_seats = adjacent_seats_func(r_idx, c_idx)

                occupied_seats = len(list(filter(lambda x: x == OCCUPIED_SEAT, adj_seats)))

                if col == EMPTY_SEAT and occupied_seats == 0:
                    new_seat_map[r_idx][c_idx] = OCCUPIED_SEAT

                    changed = True if changed is False else changed
                elif col == OCCUPIED_SEAT and occupied_seats >= occupied_seat_count:
                    new_seat_map[r_idx][c_idx] = EMPTY_SEAT

                    changed = True if changed is False else changed
                else:
                    new_seat_map[r_idx][c_idx] = col

        self.seat_map = new_seat_map

        return changed

    def part1(self, input_data: List[str]) -> int:
        changed = True

        while changed is True:
            changed = self.do_round(self.adjacent_seats, 4)

        return len([col for row in self.seat_map for col in row if col == OCCUPIED_SEAT])

    def adjacent_seats2(self, row: int, col: int) -> List[str]:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        adj_seats = []

        for dx, dy in directions:
            seat = FLOOR
            nx, ny = (row + dx), (col + dy)

            while 0 <= nx < self.rows and 0 <= ny < self.cols and seat == FLOOR:
                seat = self.seat_map[nx][ny]
                nx, ny = (nx + dx), (ny + dy)
            adj_seats.append(seat)

        return adj_seats

    def part2(self, input_data: List[str]) -> int:
        changed = True

        while changed is True:
            changed = self.do_round(self.adjacent_seats2, 5)

        return len([col for row in self.seat_map for col in row if col == OCCUPIED_SEAT])

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            'L.LL.LL.LL',
            'LLLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLLL',
            'L.LLLLLL.L',
            'L.LLLLL.LL',
        ]

        self.common(tests)
        assert self.part1(tests) == 37
        self.common(tests)
        assert self.part2(tests) == 26

        self.common(input_data)
        assert self.part1(input_data) == 2166
        self.common(input_data)
        assert self.part2(input_data) == 1955

        return 2
