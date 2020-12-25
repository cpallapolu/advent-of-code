
from collections import defaultdict
from typing import Dict, List, Tuple

from aocpuzzle import AoCPuzzle


class Tile:
    def __init__(self, directions: str) -> None:
        self.x = 0
        self.y = 0
        self.directions = directions.strip().split(' ')
        self.is_white = True
        self.direction_map = {
            'e': self.east,
            'se': self.southeast,
            'ne': self.northeast,
            'w': self.west,
            'sw': self.southwest,
            'nw': self.northwest,
        }

    def final_position(self) -> None:
        for direction in self.directions:
            self.direction_map[direction]()

    def east(self) -> None:
        self.x += 1

    def southeast(self) -> None:
        self.x += 1
        self.y -= 1

    def northeast(self) -> None:
        self.y += 1

    def west(self) -> None:
        self.x -= 1

    def southwest(self) -> None:
        self.y -= 1

    def northwest(self) -> None:
        self.x -= 1
        self.y += 1


class Puzzle24(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.tiles = []
        # white: False, black: True
        self.grid: Dict[Tuple[int, int], bool] = defaultdict(bool)
        self.neighbors = [(1, 0), (1, -1), (0, 1), (-1, 0), (0, -1), (-1, 1)]

        for line in input_data:
            line = line.replace('e', 'e ').replace('w', 'w ')
            self.tiles.append(Tile(line))

    def part1(self, input_data: List[str]) -> int:
        for tile in self.tiles:
            tile.final_position()
            self.grid[(tile.x, tile.y)] = not self.grid[(tile.x, tile.y)]

        return sum(self.grid.values())

    def count_black_tiles(self, x: int, y: int) -> int:
        return sum([
            (x + nx, y + ny) in self.grid and self.grid[(x + nx, y + ny)] is True
            for nx, ny in self.neighbors
        ])

    def part2(self, input_data: List[str]) -> int:
        self.part1(input_data)

        for _ in range(100):
            new_grid = defaultdict(bool)

            all_pos = set()

            for x, y in self.grid.keys():
                all_pos.add((x, y))
                for nx, ny in self.neighbors:
                    all_pos.add((x + nx, y + ny))

            for x, y in all_pos:
                tile = False if (x, y) not in self.grid else self.grid[(x, y)]

                neighbors = self.count_black_tiles(x, y)

                if tile is True and neighbors == 0 or neighbors > 2:
                    new_grid[(x, y)] = False
                elif tile is False and neighbors == 2:
                    new_grid[(x, y)] = True
                else:
                    new_grid[(x, y)] = tile
            self.grid = new_grid
        print(sum(self.grid.values()))
        return sum(self.grid.values())

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            'sesenwnenenewseeswwswswwnenewsewsw',
            'neeenesenwnwwswnenewnwwsewnenwseswesw',
            'seswneswswsenwwnwse',
            'nwnwneseeswswnenewneswwnewseswneseene',
            'swweswneswnenwsewnwneneseenw',
            'eesenwseswswnenwswnwnwsewwnwsene',
            'sewnenenenesenwsewnenwwwse',
            'wenwwweseeeweswwwnwwe',
            'wsweesenenewnwwnwsenewsenwwsesesenwne',
            'neeswseenwwswnwswswnw',
            'nenwswwsewswnenenewsenwsenwnesesenew',
            'enewnwewneswsewnwswenweswnenwsenwsw',
            'sweneswneswneneenwnewenewwneswswnese',
            'swwesenesewenwneswnwwneseswwne',
            'enesenwswwswneneswsenwnewswseenwsese',
            'wnwnesenesenenwwnenwsewesewsesesew',
            'nenewswnwewswnenesenwnesewesw',
            'eneswnwswnwsenenwnwnwwseeswneewsenese',
            'neswnwewnwnwseenwseesewsenwsweewe',
            'wseweeenwnesenwwwswnew',
        ]
        self.common(tests)
        assert self.part1(tests) == 10
        self.common(tests)
        assert self.part2(tests) == 2208

        self.common(input_data)
        assert self.part1(input_data) == 351
        self.common(input_data)
        assert self.part2(input_data) == 3869

        return 2
