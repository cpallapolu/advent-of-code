
from typing import List

from aocpuzzle import AoCPuzzle


class Puzzle25(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.card_pubkey, self.door_pubkey = map(int, input_data)

    def get_loop_size(self, subject_num: int, pub_key: int) -> int:
        loop_size = 0
        transformation = 1

        while transformation != pub_key:
            loop_size += 1
            transformation = (transformation * subject_num) % 20201227

        return loop_size

    def get_encryption_key(self, subject_num: int, loop_size: int) -> int:
        encrypted_key = 1

        for _ in range(loop_size):
            encrypted_key = (encrypted_key * subject_num) % 20201227

        return encrypted_key

    def part1(self) -> int:
        card_loop_size = self.get_loop_size(7, self.card_pubkey)
        door_loop_size = self.get_loop_size(7, self.door_pubkey)

        self.card_encrypted_key = self.get_encryption_key(self.door_pubkey, card_loop_size)
        self.door_encrypted_key = self.get_encryption_key(self.card_pubkey, door_loop_size)

        return self.card_encrypted_key

    def part2(self) -> str:
        return 'Congratulations!'

    def test_cases(self, input_data: List[str]) -> int:
        tests = ['5764801', '17807724']
        self.common(tests)
        assert self.part1() == 14897079
        assert self.door_encrypted_key == self.card_encrypted_key
        self.common(tests)
        assert self.part2() == 'Congratulations!'

        self.common(input_data)
        assert self.part1() == 9177528
        assert self.door_encrypted_key == self.card_encrypted_key
        self.common(input_data)
        assert self.part2() == 'Congratulations!'

        return 2
