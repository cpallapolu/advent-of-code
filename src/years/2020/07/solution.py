from collections import defaultdict
from typing import List, Set, Tuple

from aocpuzzle import AoCPuzzle


class Puzzle07(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.bags = defaultdict(list)
        self.inner_bags = defaultdict(list)

        for rule in input_data:
            outer_bag, inner_bags = rule.split(' bags contain ')

            if inner_bags == 'no other bags.':
                continue

            for inner_bag in inner_bags.split(', '):
                ob = tuple(outer_bag.split())
                ib = tuple(inner_bag.split()[:-1])

                self.bags[ob].append(ib)
                self.inner_bags[ib[1:3]].append(ob)

    def part1(self, input_data: List[str]) -> int:
        bags: Set = set()

        q, visited = [('shiny', 'gold')], []

        while len(q) > 0:
            bag = q.pop(0)

            for inner_bag in self.inner_bags[bag]:
                if inner_bag not in visited:
                    bags.add(inner_bag)
                    q.append((inner_bag[0], inner_bag[1]))
                    visited.append(bag)
        return len(bags)

    def count(self, color: Tuple[str, str]) -> int:
        bags_count = 0

        for bag in self.bags[color]:
            bags_count += int(bag[0]) + (self.count((bag[1], bag[2])) * int(bag[0]))

        return bags_count

    def part2(self, input_data: List[str]) -> int:
        return self.count(('shiny', 'gold'))

    def test_cases(self, input_data: List[str]) -> int:
        part1_tests = [
            'light red bags contain 1 bright white bag, 2 muted yellow bags.',
            'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
            'bright white bags contain 1 shiny gold bag.',
            'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
            'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
            'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
            'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
            'faded blue bags contain no other bags.',
            'dotted black bags contain no other bags.',
        ]
        part2_tests = [
            'shiny gold bags contain 2 dark red bags.',
            'dark red bags contain 2 dark orange bags.',
            'dark orange bags contain 2 dark yellow bags.',
            'dark yellow bags contain 2 dark green bags.',
            'dark green bags contain 2 dark blue bags.',
            'dark blue bags contain 2 dark violet bags.',
            'dark violet bags contain no other bags.',
        ]

        self.common(part1_tests)
        assert self.part1(part1_tests) == 4

        self.common(input_data)
        assert self.part1(input_data) == 302

        self.common(part2_tests)
        assert self.part2(part2_tests) == 126

        self.common(input_data)
        assert self.part2(input_data) == 4165

        return 3
