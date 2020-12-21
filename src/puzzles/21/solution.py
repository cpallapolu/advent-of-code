
from collections import defaultdict
from typing import List, Set

from aocpuzzle import AoCPuzzle


class Puzzle21(AoCPuzzle):
    def common(self, input_data: List[str]) -> None:
        self.ingredients = set()
        self.allergens: Set[str] = set()
        self.foods = []

        for line in input_data:
            ingredients, allergens = line.split(' (contains ')
            allergens = allergens[:-1]

            self.ingredients.update(ingredients.split(' '))
            self.allergens.update(map(lambda a: a.replace(',', ''), allergens.split(' ')))
            self.foods.append(
                (
                    ingredients.split(' '),
                    list(map(lambda x: x.replace(',', ''), allergens.split(' '))),
                ),
            )
        self.allergen_map = defaultdict(set)
        self.no_allergen_ingredients = self.ingredients.copy()

    def check_foods(self) -> None:
        for allergen in self.allergens:
            ingredient_options: Set[str] = set()

            for food_ingredients, food_allergens in self.foods:
                # if the allergen is in this food too, get the common(intersection) of current
                # ingredient_options and the ingredients of the food
                if allergen in food_allergens:
                    if len(ingredient_options) == 0:
                        ingredient_options = set(food_ingredients)
                    else:
                        ingredient_options = ingredient_options.intersection(food_ingredients)

            self.allergen_map[allergen] = ingredient_options

            for ingredient_option in ingredient_options:
                self.no_allergen_ingredients.discard(ingredient_option)

    def part1(self, input_data: List[str]) -> int:
        self.check_foods()

        num_ingredients = 0
        for no_allergen_ingredient in self.no_allergen_ingredients:
            for food_ingredients, _ in self.foods:
                if no_allergen_ingredient in food_ingredients:
                    num_ingredients += 1

        return num_ingredients

    def part2(self, input_data: List[str]) -> str:
        self.check_foods()
        ingredient_allergen = defaultdict(str)
        allergens = list(self.allergen_map.keys())

        while len(allergens) > 0:
            for allergen in allergens:
                if len(self.allergen_map[allergen]) == 1:
                    ingredient_allergen[allergen] = self.allergen_map[allergen].pop()
                    allergens.remove(allergen)

                    for a in allergens:
                        if ingredient_allergen[allergen] in self.allergen_map[a]:
                            self.allergen_map[a].remove(ingredient_allergen[allergen])
                    continue

        return ','.join(
            map(
                lambda am: am[1],
                sorted(ingredient_allergen.items(), key=lambda x: x[0]),
            ),
        )

    def test_cases(self, input_data: List[str]) -> int:
        tests = [
            'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
            'trh fvjkl sbzzf mxmxvkd (contains dairy)',
            'sqjhc fvjkl (contains soy)',
            'sqjhc mxmxvkd sbzzf (contains fish)',
        ]
        self.common(tests)
        assert self.part1(tests) == 5

        self.common(tests)
        assert self.part2(tests) == 'mxmxvkd,sqjhc,fvjkl'

        self.common(input_data)
        assert self.part1(input_data) == 2317

        self.common(input_data)
        assert self.part2(input_data) == 'kbdgs,sqvv,slkfgq,vgnj,brdd,tpd,csfmb,lrnz'
        return 2
