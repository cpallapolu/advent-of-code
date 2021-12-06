

from collections import defaultdict

from aocpuzzle import AoCPuzzle


class BingoBoard:
    def __init__(self, board: list[str]) -> None:
        self.positions: dict[int, list[int]] = defaultdict(list)
        self.bingo = {
            'row': [0, 0, 0, 0, 0],
            'col': [0, 0, 0, 0, 0],
            'diag': [0, 0],
        }

        self.board = [[0] * 5 for _ in range(5)]
        self.last_choice = 0
        self.init_board(board)

    def init_board(self, board: list[str]) -> None:
        for row_idx, row in enumerate(board):
            for col_idx, choice in enumerate(' '.join(row.split()).split(' ')):
                int_choice = int(choice)
                self.board[row_idx][col_idx] = int_choice
                self.positions[int_choice] = [row_idx, col_idx]

    def update_board(self, choice: int) -> None:
        if choice in self.positions:
            self.last_choice = choice
            [row, col] = self.positions[choice]

            self.board[row][col] = -1
            self.update_bingo(row, col)

    def update_bingo(self, row: int, col: int) -> None:
        self.bingo['row'][row] += 1
        self.bingo['col'][col] += 1

        if row == col == 2:
            self.bingo['diag'][0] += 1
            self.bingo['diag'][1] += 1
        elif row == col:
            self.bingo['diag'][0] += 1
        elif row + col == 4:
            self.bingo['diag'][1] += 1

    def check_bingo(self, complete_board=False) -> bool:
        return 5 in self.bingo['row'] or 5 in self.bingo['col']

    def unmarked_choices_sum(self) -> int:
        return sum([
            int(choice)
            for row in self.board
            for choice in row
            if choice != -1
        ])


class Puzzle04(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.drawn_choices = list(map(int, input_data[0].split(',')))

        self.boards: list[BingoBoard] = [
            BingoBoard(row.split('|'))
            for row in '|'.join(input_data[2:]).split('||')
        ]

        self.won_boards: list[BingoBoard] = []

    def update_boards(self, choice: int) -> None:
        for idx in range(len(self.boards) - 1, -1, -1):
            board = self.boards[idx]

            board.update_board(choice)
            if board.check_bingo():
                self.won_boards.append(board)
                self.boards.pop(idx)

    def part1(self) -> int:
        for drawn_choice in self.drawn_choices:
            if len(self.boards) == 0:
                break

            self.update_boards(drawn_choice)

        first_won_board = self.won_boards[0]

        return first_won_board.unmarked_choices_sum() * first_won_board.last_choice

    def part2(self) -> int:
        for drawn_choice in self.drawn_choices:
            if len(self.boards) == 0:
                break

            self.update_boards(drawn_choice)

        last_won_board = self.won_boards[-1]

        return last_won_board.unmarked_choices_sum() * last_won_board.last_choice

    def test_cases(self, input_data: list[str]) -> int:
        tests = [
            [
                '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
                '',
                '22 13 17 11  0',
                ' 8  2 23  4 24',
                '21  9 14 16  7',
                ' 6 10  3 18  5',
                ' 1 12 20 15 19',
                '',
                ' 3 15  0  2 22',
                ' 9 18 13 17  5',
                '19  8  7 25 23',
                '20 11 10 24  4',
                '14 21 16 12  6',
                '',
                '14 21 17 24  4',
                '10 16 15  9 19',
                '18  8 23 26 20',
                '22 11 13  6  5',
                ' 2  0 12  3  7',
            ],
        ]
        for test in tests:
            self.common(test)
            assert self.part1() == 4512
            self.common(test)
            assert self.part2() == 1924

        self.common(input_data)
        assert self.part1() == 82440
        self.common(input_data)
        assert self.part2() == 20774

        return len(tests) + 1
