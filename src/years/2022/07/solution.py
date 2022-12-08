

from collections import defaultdict

from aocpuzzle import AoCPuzzle

DOLLAR = '$'
CD_CMD = '$ cd'
BACK_DIR_CMD = '$ cd ..'
LS_CMD = '$ ls'
BACK_DIR = '..'
DIR_OUTPUT = 'dir '


class Puzzle07(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.directory_sizes: dict[str, int] = defaultdict(int)

        curr_working_dir: list[str] = []

        for cmd in input_data:
            if cmd == BACK_DIR_CMD:
                curr_working_dir.pop(-1)
            elif cmd.startswith(CD_CMD):
                curr_working_dir.append(cmd.split().pop(-1))
            elif cmd.startswith(LS_CMD) or cmd.startswith(DIR_OUTPUT):
                continue
            else:
                for idx in range(len(curr_working_dir)):
                    self.directory_sizes['/'.join(curr_working_dir[:idx + 1])] += int(cmd.split().pop(0))

    def part1(self) -> int:
        return sum(size for size in self.directory_sizes.values() if size <= 100_000)

    def part2(self) -> int:
        return min(
            size
            for size in self.directory_sizes.values() if size > 30_000_000 - (70_000_000 - self.directory_sizes['/'])
        )

    def test_cases(self, input_data: list[str]) -> int:
        print()
        tests: list[dict] = [
            {
                'input_data': [
                    '$ cd /',
                    '$ ls',
                    'dir a',
                    '14848514 b.txt',
                    '8504156 c.dat',
                    'dir d',
                    '$ cd a',
                    '$ ls',
                    'dir e',
                    '29116 f',
                    '2557 g',
                    '62596 h.lst',
                    '$ cd e',
                    '$ ls',
                    '584 i',
                    '$ cd ..',
                    '$ cd ..',
                    '$ cd d',
                    '$ ls',
                    '4060174 j',
                    '8033020 d.log',
                    '5626152 d.ext',
                    '7214296 k',
                ],
                'part1': 95437,
                'part2': 24933642,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 1350966
        self.common(input_data)
        assert self.part2() == 6296435

        return len(tests) + 1
