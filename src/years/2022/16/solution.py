

from collections import defaultdict
from re import fullmatch

from aocpuzzle import AoCPuzzle

LINE_REGEX = 'Valve ([A-Z]{2}) has flow rate=([0-9]*); tunnels? leads? to valves? ([A-Z]{2}.*)$'


class Puzzle16(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.starting_tunnel = 'AA'

        self.valves: dict[str, int] = defaultdict(int)
        self.distances: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(lambda: 9999))

        for line in input_data:
            valve, flow_rate, tunnels = fullmatch(LINE_REGEX, line).groups()  # noqa T484

            self.valves[valve] = int(flow_rate)
            self.distances[valve][valve] = 0
            for tunnel in tunnels.split(', '):
                self.distances[valve][tunnel] = 1

        for k in self.valves:
            for i in self.valves:
                for j in self.valves:
                    self.distances[i][j] = min(
                        self.distances[i][j],
                        self.distances[i][k] + self.distances[k][j],
                    )

    def traverse(self, valve: str, curr_time: int, remaining_tunnels_with_flow_rate: frozenset, elephant: bool):
        ans = self.traverse(self.starting_tunnel, 26, remaining_tunnels_with_flow_rate, False) if elephant else 0

        for tunnel in remaining_tunnels_with_flow_rate:
            next_tunnel = curr_time - self.distances[valve][tunnel] - 1
            if next_tunnel >= 0:
                ans = max(
                    ans,
                    sum([
                        self.valves[tunnel] * next_tunnel,
                        self.traverse(tunnel, next_tunnel, remaining_tunnels_with_flow_rate - {tunnel}, elephant),
                    ]),
                )
        return ans

    def part1(self) -> int:
        tunnels_with_flow_rate = frozenset(x for x in self.valves if self.valves[x] > 0)

        return self.traverse(self.starting_tunnel, 30, tunnels_with_flow_rate, False)

    def part2(self) -> int:
        tunnels_with_flow_rate = frozenset(x for x in self.valves if self.valves[x] > 0)

        return self.traverse(self.starting_tunnel, 26, tunnels_with_flow_rate, True)

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
                    'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
                    'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
                    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
                    'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
                    'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
                    'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
                    'Valve HH has flow rate=22; tunnel leads to valve GG',
                    'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
                    'Valve JJ has flow rate=21; tunnel leads to valve II',
                ],
                'part1': 1651,
                'part2': 1707,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 2029
        self.common(input_data)
        assert self.part2() == 2723

        return len(tests) + 1
