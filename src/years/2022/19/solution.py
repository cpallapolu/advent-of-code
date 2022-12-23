

from collections import deque
from math import prod
from re import findall

from aocpuzzle import AoCPuzzle


class Blueprint:
    def __init__(
        self,
        idx: int,
        ores_for_ore_robot: int,
        ores_for_clay_robot: int,
        ores_for_obsidian_robot: int,
        clays_for_obsidian_robot: int,
        ores_for_geode_robot: int,
        obsidians_for_geode_robot: int,
    ) -> None:
        self.id = idx
        self.ores_for_ore_robot_cost = ores_for_ore_robot
        self.ores_clay_robot_cost = ores_for_clay_robot
        self.ores_for_obsidian_robot_cost = ores_for_obsidian_robot
        self.clays_for_obsidian_robot_cost = clays_for_obsidian_robot
        self.ores_for_geodes_robot_cost = ores_for_geode_robot
        self.obsidians_for_geodes_robot_cost = obsidians_for_geode_robot

    def __repr__(self):
        return '|'.join((
            str(self.id),
            str(self.ore_robot_cost),
            str(self.ores_clay_robot_cost),
            str(self.ores_for_obsidian_robot_cost),
            str(self.clays_for_obsidian_robot_cost),
            str(self.ores_for_geodes_robot_cost),
            str(self.ores_for_geodes_robot_cost),
        ))


class Puzzle19(AoCPuzzle):
    def common(self, input_data: list[str]) -> None:
        self.blueprints = []
        for blueprint in input_data:
            (
                idx,
                ore_cost,
                clay_cost,
                ore_for_obsidian_cost,
                clay_for_obsidian_cost,
                ore_for_geode_cost,
                obsidian_for_geode,
            ) = list(map(int, findall(r'-?[0-9]+', blueprint)))

            self.blueprints.append(
                Blueprint(
                    idx, ore_cost, clay_cost, ore_for_obsidian_cost,
                    clay_for_obsidian_cost, ore_for_geode_cost, obsidian_for_geode,
                ),
            )

    def mine_geodes(self, blueprint: Blueprint, minutes: int) -> int:
        queue = deque(['|'.join(map(str, (0, 0, 0, 0, 1, 0, 0, 0, minutes)))])

        max_ore_to_spend = max(
            blueprint.ores_for_ore_robot_cost,
            blueprint.ores_clay_robot_cost,
            blueprint.ores_for_obsidian_robot_cost,
            blueprint.ores_for_geodes_robot_cost,
        )
        max_clay = blueprint.clays_for_obsidian_robot_cost
        max_geodes = 0
        states = set()

        while len(queue) > 0:
            curr = queue.popleft()
            (
                collected_ore,
                collected_clay,
                collected_obsidian,
                collected_geode,
                robots_ore,
                robots_clay,
                robots_obsidian,
                robots_geode,
                minute,
            ) = map(int, curr.split('|'))

            if minute == 0:
                max_geodes = max(max_geodes, collected_geode)
                continue

            robots_ore = min(max_ore_to_spend, robots_ore)
            robots_clay = min(max_clay, robots_clay)
            robots_obsidian = min(blueprint.obsidians_for_geodes_robot_cost, robots_obsidian)

            collected_ore = min(collected_ore, minute * max_ore_to_spend - robots_ore * (minute - 1))
            collected_clay = min(collected_clay, minute * max_clay - robots_clay * (minute - 1))
            collected_obsidian = min(
                collected_obsidian,
                minute * blueprint.obsidians_for_geodes_robot_cost - robots_obsidian * (minute - 1),
            )
            state_key = '|'.join(map(str, (collected_ore, collected_clay, collected_obsidian, collected_geode,
                                           robots_ore, robots_clay, robots_obsidian, robots_geode, minute)))
            if state_key in states:
                continue

            states.add(state_key)

            if (
                collected_ore >= blueprint.ores_for_geodes_robot_cost
                and collected_obsidian >= blueprint.obsidians_for_geodes_robot_cost
            ):
                state = (
                    collected_ore + robots_ore - blueprint.ores_for_geodes_robot_cost,
                    collected_clay + robots_clay,
                    collected_obsidian + robots_obsidian - blueprint.obsidians_for_geodes_robot_cost,
                    collected_geode + robots_geode,
                    robots_ore,
                    robots_clay,
                    robots_obsidian,
                    robots_geode + 1,
                    minute - 1,
                )
                queue.append('|'.join(map(str, state)))
            else:
                new_queues = [(
                    collected_ore + robots_ore,
                    collected_clay + robots_clay,
                    collected_obsidian + robots_obsidian,
                    collected_geode + robots_geode,
                    robots_ore,
                    robots_clay,
                    robots_obsidian,
                    robots_geode,
                    minute - 1,
                )]

                if (
                    collected_ore >= blueprint.ores_for_obsidian_robot_cost
                    and collected_clay >= blueprint.clays_for_obsidian_robot_cost
                ):
                    new_queues.append((
                        collected_ore + robots_ore - blueprint.ores_for_obsidian_robot_cost,
                        collected_clay + robots_clay - blueprint.clays_for_obsidian_robot_cost,
                        collected_obsidian + robots_obsidian,
                        collected_geode + robots_geode,
                        robots_ore,
                        robots_clay,
                        robots_obsidian + 1,
                        robots_geode,
                        minute - 1,
                    ))
                if collected_ore >= blueprint.ores_clay_robot_cost:
                    new_queues.append((
                        collected_ore + robots_ore - blueprint.ores_clay_robot_cost,
                        collected_clay + robots_clay,
                        collected_obsidian + robots_obsidian,
                        collected_geode + robots_geode,
                        robots_ore,
                        robots_clay + 1,
                        robots_obsidian,
                        robots_geode,
                        minute - 1,
                    ))
                if collected_ore >= blueprint.ores_for_ore_robot_cost:
                    new_queues.append((
                        collected_ore + robots_ore - blueprint.ores_for_ore_robot_cost,
                        collected_clay + robots_clay,
                        collected_obsidian + robots_obsidian,
                        collected_geode + robots_geode,
                        robots_ore + 1,
                        robots_clay,
                        robots_obsidian,
                        robots_geode,
                        minute - 1,
                    ))
                queue.extend(map(lambda nq: '|'.join(map(str, nq)), new_queues))

        return max_geodes

    def simulate_mining(self, minutes: int, max_blueprints: int) -> list[int]:
        blueprints = self.blueprints[:max_blueprints]

        return [
            self.mine_geodes(blueprint, minutes)
            for blueprint in blueprints
        ]

    def part1(self) -> int:
        return sum([
            idx * score
            for idx, score in enumerate(self.simulate_mining(24, len(self.blueprints)), start=1)
        ])

    def part2(self) -> int:
        return prod([
            score
            for score in self.simulate_mining(32, 3)
        ])

    def test_cases(self, input_data: list[str]) -> int:
        tests: list[dict] = [
            {
                'input_data': [
                    'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 \
                        ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.',
                    'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 \
                        ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.',
                ],
                'part1': 33,
                'part2': 3472,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 1624
        self.common(input_data)
        assert self.part2() == 12628

        return len(tests) + 1
