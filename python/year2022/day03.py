import time
import os


def char_to_priority(item: str) -> int:
    item = ord(item)
    if item >= 97:  # this means it's lowercase: ord('a') = 97
        item -= 96  # correct priority for a = 1; 97 - 96 = 1
    else:
        item -= 38  # ord('A') = 65; correct priority for A = 27; 65 - 39 = 27
    return item


class Rucksack:
    def __init__(self, contents: str):
        assert len(contents) % 2 == 0, "I didn't think it was possible for a line of the input to have an odd length"
        contents2 = []
        for item in contents:
            contents2.append(char_to_priority(item))
        self.compartment1 = set(contents2[0:len(contents) // 2])
        self.compartment2 = set(contents2[len(contents) // 2:])
        # Union outputs a set containing all elements appearing in any of the input sets, i.e. combining them.
        self.full_contents = self.compartment1.union(self.compartment2)


def parse_input(filename: str) -> list[Rucksack]:
    sacks = []
    with open(filename, "r") as file:
        for line in file:
            sacks.append(Rucksack(line.strip()))
    return sacks


def get_compartment_shared_total(sacks: list[Rucksack]) -> int:  # Part 1
    total = 0
    for sack in sacks:
        # intersection finds the intersection of the two sets,
        # that is, it outputs a set containing only what's in both input sets.
        for i in sack.compartment1.intersection(sack.compartment2):
            total += i
    return total


def get_badge_total(sacks: list[Rucksack]) -> int:  # Part 2
    # Split into groups of 3
    groups: list[list[Rucksack]] = []
    group: list[Rucksack] = []
    for i, sack in enumerate(sacks):
        group.append(sack)
        if i % 3 == 2:
            groups.append(group)
            group = []

    # Find the badges within each group
    total = 0
    for group in groups:
        temp = group[0].full_contents.intersection(group[1].full_contents, group[2].full_contents)
        for i in temp:
            total += i

    return total


def main(input_filename: str):
    start_time = time.time()
    sacks = parse_input(input_filename)
    part1_start = time.time()
    pt1 = get_compartment_shared_total(sacks)
    part2_start = time.time()
    pt2 = get_badge_total(sacks)
    end_time = time.time()
    print(f"Part 1: Sum of priorities of shared compartment items: {pt1}")
    print(f"Part 2: Sum of priorities of badges: {pt2}")

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")
    return


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day03.txt")

    run_main()
