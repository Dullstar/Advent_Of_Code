import time
import os


# So, it turned out we didn't need to keep track of the food items the elves were carrying and just needed the total
# amount of food, but I wanted to avoid needing to rewrite parse_input if Part 2 had called for it.
# I could refactor it to only track the totals as a plain old int now that I *know* I don't need to keep track of
# the individual counts, but at least for now I'm not going to. Maybe I will later.

class Elf:
    def __init__(self, food: list[int]):
        self.food_items: list[int] = food
        self.food_total: int = sum(food)


def parse_input(filename: str):
    elves = []
    with open(filename, "r") as file:
        contents = file.read().strip().split("\n\n")
        for elf in contents:
            elf = elf.split("\n")
            elf_food = []
            for food in elf:
                elf_food.append(int(food))
            elves.append(Elf(elf_food))
    return elves


def main(input_filename: str):
    start_time = time.time()
    elves = parse_input(input_filename)
    part1_start = time.time()
    elves.sort(key=lambda elf: elf.food_total, reverse=True)
    pt1 = elves[0].food_total
    part2_start = time.time()
    pt2 = elves[0].food_total + elves[1].food_total + elves[2].food_total
    end_time = time.time()
    print(f"The elf with the most food is carrying {pt1} kcal")
    print("The 3 elves with the most food are carrying:")
    print(f"    {elves[0].food_total} + {elves[1].food_total} + {elves[2].food_total} = {pt2} kcal")

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")

    return


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day01.txt")

    run_main()
