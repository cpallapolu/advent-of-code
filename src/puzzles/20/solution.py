from math import prod
from typing import Callable, List, Union

from aocpuzzle import AoCPuzzle


class Tile:
    def __init__(self, tile_row: str) -> None:
        [tile_id, *tile] = tile_row.split('\n')

        self.id = int(tile_id.split(' ')[1].replace(':', ''))
        self.tile = tile
        self.rotations: List[List[str]] = []
        self.borders: List[str] = []


Tiles = List[Tile]


class Puzzle20(AoCPuzzle):
    def top_border(self, tile: List[str]) -> str:
        return ''.join(tile[0])

    def bottom_border(self, tile: List[str]) -> str:
        return ''.join(tile[-1])

    def left_border(self, tile: List[str]) -> str:
        return ''.join(t[0] for t in tile)

    def right_border(self, tile: List[str]) -> str:
        return ''.join(t[-1] for t in tile)

    def mirror(self, tile: List[str]) -> List[str]:
        return [''.join(list(t)[::-1]) for t in tile]

    def rotate(self, tile: List[str]) -> List[str]:
        return self.mirror([
            ''.join([x[idx] for x in tile])
            for idx, _ in enumerate(tile)
        ])

    def all_rotations(self, tile: List[str]) -> List[List[str]]:
        rotations = [tile, self.mirror(tile)]
        curr_rotation = tile

        for _ in range(3):
            curr_rotation = self.rotate(curr_rotation)

            rotations.extend([curr_rotation, self.mirror(curr_rotation)])

        return rotations

    def find_rotation(self, tile: Union[Tile, None], func: Callable) -> List[str]:
        if tile is not None:
            return [rotation for rotation in tile.rotations if func(rotation) is True][0]
        return []

    def common(self, input_data: List[str]) -> None:
        input_data = '\n'.join(input_data[:-1]).split('\n\n')
        self.tiles: Tiles = []

        for line in input_data:
            tile = Tile(line)
            rotations = self.all_rotations(tile.tile)
            tile.rotations = rotations
            tile.borders = [self.top_border(rotation) for rotation in rotations]

            self.tiles.append(tile)

        self.monster = [
            '                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   ',
        ]
        self.monster_size = ''.join(self.monster).count('#')

    def find_corners(self) -> List[Tile]:
        corners = []

        for outer_tile in self.tiles:
            matching = []
            for inner_tile in self.tiles:
                if outer_tile.id != inner_tile.id:
                    for border in inner_tile.borders:
                        if border in outer_tile.borders:
                            matching.append(inner_tile)

            if len(set(matching)) == 2:
                corners.append(outer_tile)

        return corners

    def part1(self, input_data: List[str]) -> int:
        corners = self.find_corners()

        return prod([c.id for c in corners])

    def find_tile(self, func: Callable) -> Union[Tile, None]:
        for tile in self.tiles:
            if func(tile) is True:
                self.tiles.remove(tile)
                return tile
        return None

    def build_tile_map(self) -> None:
        tile_map: List[List[List[str]]] = [[]]

        first_tile = self.find_tile(lambda t: t.id == self.corners[0].id)

        if first_tile is not None:
            for rotation in first_tile.rotations:
                top_border = self.top_border(rotation)
                left_border = self.left_border(rotation)
                matching = 0
                for tile in self.tiles:
                    matching += any([top_border in tile.borders, left_border in tile.borders])

                if matching == 0:
                    break

        next_tile = rotation

        while next_tile:
            right = self.right_border(next_tile)
            tile_map[len(tile_map) - 1].append(next_tile)

            next_tile = self.find_rotation(
                self.find_tile(lambda t: right in t.borders),
                lambda t: self.left_border(t) == right,
            )

            if len(next_tile) == 0:
                bottom = self.bottom_border(tile_map[len(tile_map) - 1][0])
                tile_map.append([])

                next_tile = self.find_rotation(
                    self.find_tile(lambda t: bottom in t.borders),
                    lambda t: self.top_border(t) == bottom,
                )
        tile_map.pop()

        self.tile_map = tile_map

    def count_monsters(self, image: List[str]) -> int:
        monster_locs = []
        max_x, max_y = 0, 0

        for my, line in enumerate(self.monster):
            for mx, c in enumerate(line):
                if c == '#':
                    monster_locs.append((mx, my))
                    max_x, max_y = max(mx, max_x), max((my, max_y))
        count = 0

        for y in range(len(image)):
            if y + max_y >= len(image):
                break

            for x in range(len(image[y])):
                if x + max_x >= len(image[y]):
                    break

                has_monster = True

                for mx, my in monster_locs:
                    if image[y + my][x + mx] != '#':
                        has_monster = False
                        break
                if has_monster:
                    count += 1
        return count * self.monster_size

    def part2(self, input_data: List[str]) -> int:
        self.corners = self.find_corners()
        self.build_tile_map()

        self.stripped_tile_map = [
            [[t[1:-1] for t in tile[1:-1]] for tile in row]
            for row in self.tile_map
        ]
        self.image = []

        for row in self.stripped_tile_map:
            new_row = ['' for _ in range(len(row[0][0]))]

            while len(row) > 0:
                tile = row.pop(0)
                for idx, t in enumerate(tile):
                    new_row[idx] += t

            self.image.extend(new_row)

        monsters = sum([self.count_monsters(r) for r in self.all_rotations(self.image)])

        return ''.join(self.image).count('#') - monsters

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            'Tile 2311:',
            '..##.#..#.',
            '##..#.....',
            '#...##..#.',
            '####.#...#',
            '##.##.###.',
            '##...#.###',
            '.#.#.#..##',
            '..#....#..',
            '###...#.#.',
            '..###..###',
            '',
            'Tile 1951:',
            '#.##...##.',
            '#.####...#',
            '.....#..##',
            '#...######',
            '.##.#....#',
            '.###.#####',
            '###.##.##.',
            '.###....#.',
            '..#.#..#.#',
            '#...##.#..',
            '',
            'Tile 1171:',
            '####...##.',
            '#..##.#..#',
            '##.#..#.#.',
            '.###.####.',
            '..###.####',
            '.##....##.',
            '.#...####.',
            '#.##.####.',
            '####..#...',
            '.....##...',
            '',
            'Tile 1427:',
            '###.##.#..',
            '.#..#.##..',
            '.#.##.#..#',
            '#.#.#.##.#',
            '....#...##',
            '...##..##.',
            '...#.#####',
            '.#.####.#.',
            '..#..###.#',
            '..##.#..#.',
            '',
            'Tile 1489:',
            '##.#.#....',
            '..##...#..',
            '.##..##...',
            '..#...#...',
            '#####...#.',
            '#..#.#.#.#',
            '...#.#.#..',
            '##.#...##.',
            '..##.##.##',
            '###.##.#..',
            '',
            'Tile 2473:',
            '#....####.',
            '#..#.##...',
            '#.##..#...',
            '######.#.#',
            '.#...#.#.#',
            '.#########',
            '.###.#..#.',
            '########.#',
            '##...##.#.',
            '..###.#.#.',
            '',
            'Tile 2971:',
            '..#.#....#',
            '#...###...',
            '#.#.###...',
            '##.##..#..',
            '.#####..##',
            '.#..####.#',
            '#..#.#..#.',
            '..####.###',
            '..#.#.###.',
            '...#.#.#.#',
            '',
            'Tile 2729:',
            '...#.#.#.#',
            '####.#....',
            '..#.#.....',
            '....#..#.#',
            '.##..##.#.',
            '.#.####...',
            '####.#.#..',
            '##.####...',
            '##..#.##..',
            '#.##...##.',
            '',
            'Tile 3079:',
            '#.#.#####.',
            '.#..######',
            '..#.......',
            '######....',
            '####.#..#.',
            '.#...#.##.',
            '#.#####.##',
            '..#.###...',
            '..#.......',
            '..#.###...',
            '',
        ]

        self.common(tests)
        assert self.part1(tests) == 20899048083289
        assert self.part2(tests) == 273

        self.common(input_data)
        assert self.part1(input_data) == 7492183537913

        return 2
