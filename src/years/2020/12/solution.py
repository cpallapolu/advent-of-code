from typing import List

from aocpuzzle import AoCPuzzle


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Puzzle12(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.navigations = [(n[0], int(n[1:])) for n in input_data]
        self.direction = 90

    def action(self, action: str, value: int) -> None:
        if action == 'N':
            self.pos.y += value
        elif action == 'S':
            self.pos.y -= value
        elif action == 'E':
            self.pos.x += value
        elif action == 'W':
            self.pos.x -= value
        elif action == 'L':
            self.direction = (self.direction - value) % 360
        elif action == 'R':
            self.direction = (self.direction + value) % 360
        elif action == 'F':
            self.forward(value)

    def forward(self, value: int) -> None:
        if self.direction == 0:
            self.action('N', value)
        elif self.direction == 90:
            self.action('E', value)
        elif self.direction == 180:
            self.action('S', value)
        elif self.direction == 270:
            self.action('W', value)

    def part1(self, input_data: List[str]) -> int:
        self.pos = Position(0, 0)

        for (action, value) in self.navigations:
            self.action(action, value)

        return abs(self.pos.x) + abs(self.pos.y)

    def action_2(self, action: str, value: int) -> None:
        if action == 'N':
            self.waypoint.y += value
        elif action == 'S':
            self.waypoint.y -= value
        elif action == 'E':
            self.waypoint.x += value
        elif action == 'W':
            self.waypoint.x -= value
        elif action == 'L':
            for _ in range(value // 90):
                self.waypoint.x, self.waypoint.y = -self.waypoint.y, self.waypoint.x
        elif action == 'R':
            for _ in range(value // 90):
                self.waypoint.x, self.waypoint.y = self.waypoint.y, -self.waypoint.x
        elif action == 'F':
            self.pos.x += (self.waypoint.x * value)
            self.pos.y += (self.waypoint.y * value)

    def part2(self, input_data: List[str]) -> int:
        self.pos = Position(0, 0)
        self.waypoint = Position(10, 1)

        for (action, value) in self.navigations:
            self.action_2(action, value)

        return abs(self.pos.x) + abs(self.pos.y)

    def test_cases(self, input_data: List[str]) -> int:
        tests = ['F10', 'N3', 'F7', 'R90', 'F11']
        self.common(tests)
        assert self.part1(tests) == 25
        assert self.part2(tests) == 286

        self.common(input_data)
        assert self.part1(input_data) == 2847
        assert self.part2(input_data) == 29839

        return 2
