
from collections import defaultdict

from aocpuzzle import AoCPuzzle


class Puzzle12(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.cave_paths: dict[str, set[str]] = defaultdict(set)

        for cave_path in input_data:
            start, end = cave_path.split('-')

            if start != 'start':
                self.cave_paths[end].add(start)

            if end != 'start':
                self.cave_paths[start].add(end)

    def dfs(self, cave: str, visited_caves: set[str], can_visit_small_cave_twice: bool) -> int:
        if cave == 'end':
            return 1

        total_paths = 0

        for cave in self.cave_paths[cave]:
            # You can visit either UPPER cave or a non visited LOWER cave
            if cave.isupper() is True or (cave.islower() is True and cave not in visited_caves):
                total_paths += self.dfs(cave, visited_caves | {cave}, can_visit_small_cave_twice)
            # You can visit one LOWER cave twice.
            elif cave.islower() is True and cave in visited_caves and can_visit_small_cave_twice:
                total_paths += self.dfs(cave, visited_caves | {cave}, False)

        return total_paths

    def part1(self) -> int:
        return self.dfs('start', set(), False)

    def part2(self) -> int:
        return self.dfs('start', set(), True)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'start-A',
                    'start-b',
                    'A-c',
                    'A-b',
                    'b-d',
                    'A-end',
                    'b-end',
                ],
                'part1': 10,
                'part2': 36,
            },
            {
                'input_data': [
                    'dc-end',
                    'HN-start',
                    'start-kj',
                    'dc-start',
                    'dc-HN',
                    'LN-dc',
                    'HN-end',
                    'kj-sa',
                    'kj-HN',
                    'kj-dc',
                ],
                'part1': 19,
                'part2': 103,
            },
            {
                'input_data': [
                    'fs-end',
                    'he-DX',
                    'fs-he',
                    'start-DX',
                    'pj-DX',
                    'end-zg',
                    'zg-sl',
                    'zg-pj',
                    'pj-he',
                    'RW-he',
                    'fs-DX',
                    'pj-RW',
                    'zg-RW',
                    'start-pj',
                    'he-WI',
                    'zg-he',
                    'pj-fs',
                    'start-RW',
                ],
                'part1': 226,
                'part2': 3509,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 3485
        self.common(input_data)
        assert self.part2() == 85062

        return len(tests) + 1
