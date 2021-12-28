
from heapq import heapify, heappop, heappush

from aocpuzzle import AoCPuzzle

ROOM_X = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8,
}

MOVE_COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

STOPPABLE = [0, 1, 3, 5, 7, 9, 10]
PosType = tuple[int, int]


class Puzzle23(AoCPuzzle):
    def dijkstra(self, amphipods):
        q = [
            (0, 0, (amphipods, (None, None, None, None, None, None, None, None, None, None, None))),
        ]

        heapify(q)

        seen = set()

        while len(q) > 0:
            cost, _, (rooms, hallway) = heappop(q)
            if all(
                all(amphipod == chr(idx + 65) for amphipod in room)
                for idx, room in enumerate(rooms)
            ):
                return cost

            if (rooms, hallway) in seen:
                continue

            seen.add((rooms, hallway))

            # Move an amphipod from a room into the hallway.
            for i, room in enumerate(rooms):
                # We can only move the first amphipod in each room; the others are
                # stuck.
                try:
                    j, amphipod = next((j, amphipod) for j, amphipod in enumerate(room) if amphipod)
                except StopIteration:
                    continue

                # If this amphipod, and all others behind it, are in the correct
                # room, then don't move.
                if all(room[k] == chr(i + 65) for k in range(j, len(room))):
                    continue

                # We can move to any non-junction cell in the hallway.
                for p in STOPPABLE:
                    # Check if path is obstructed.
                    p1, p2 = 2 * i + 2, p
                    if p1 > p2:
                        p1, p2 = p2, p1

                    if any(hallway[k] is not None for k in range(p1, p2 + 1)):
                        continue

                    _cost = cost + MOVE_COST[amphipod] * (j + p2 - p1 + 1)
                    _rooms = tuple(
                        tuple(
                            None if (i_ == i and j_ == j) else amphipod
                            for j_, amphipod in enumerate(room)
                        )
                        for i_, room in enumerate(rooms)
                    )
                    _hallway = tuple(
                        amphipod if p_ == p else h
                        for p_, h in enumerate(hallway)
                    )

                    heappush(q, (_cost, id(_rooms), (_rooms, _hallway)))

            # Move an amphibian from the hallway into their room.
            for p in STOPPABLE:
                amphipod = hallway[p]
                if amphipod is None:
                    continue

                # Check if path is obstructed.
                p1, p2 = ROOM_X[amphipod], p
                if p < ROOM_X[amphipod]:
                    p1, p2 = p2 + 1, p1 + 1

                if all(hallway[k] is None for k in range(p1, p2)):
                    i = ord(amphipod) - 65
                    room = rooms[i]

                    # Check if the room is safe to enter.
                    if any(c is not None and c != amphipod for c in room):
                        continue

                    # Go as far in as possible!
                    try:
                        j = next(j for j, c in enumerate(room) if c is not None) - 1
                    except StopIteration:
                        j = len(room) - 1

                    _cost = cost + MOVE_COST[amphipod] * (j + abs(ROOM_X[amphipod] - p) + 1)
                    _rooms = tuple(
                        tuple(
                            amphipod if (k == i and idx == j) else h
                            for idx, h in enumerate(room)
                        )
                        for k, room in enumerate(rooms)
                    )
                    _hallway = tuple(
                        None if k == p else h
                        for k, h in enumerate(hallway)
                    )

                    heappush(q, (_cost, id(_rooms), (_rooms, _hallway)))

    def common(self, input_data: list[str]) -> None:
        self.locations = [list(ln) for ln in input_data]
        self.rooms = tuple([
            (self.locations[2][idx], self.locations[3][idx])
            for idx in [3, 5, 7, 9]
        ])

    def part1(self) -> int:
        return self.dijkstra(self.rooms)

    def part2(self) -> int:
        rooms = tuple([
            (self.rooms[idx][0], *new_room, self.rooms[idx][1])
            for idx, new_room in enumerate(['DD', 'CB', 'BA', 'AC'])
        ])

        return self.dijkstra(rooms)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    '#############',
                    '#...........#',
                    '###B#C#B#D###',
                    '###A#D#C#A###',
                    '#############',
                ],
                'part1': 12521,
                'part2': 44169,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 15365
        self.common(input_data)
        assert self.part2() == 52055

        return len(tests) + 1
