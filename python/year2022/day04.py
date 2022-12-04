import time
import os
import itertools
import re
import collections


ElfPair = collections.namedtuple("ElfPair", ["elf1", "elf2"])


class SectionAssignment:
    def __init__(self, start, end):
        self.start = min(start, end)
        self.end = max(start, end)

    # Returns true iff this assignment fully contains the other assignment.
    def contains(self, other):
        return (other.start >= self.start) and (other.end <= self.end)

    # Returns true iff this assignment fully contains, or is fully contained by, the other assignment.
    def either_contains(self, other):
        return self.contains(other) or other.contains(self)

    def overlaps(self, other):
        # I think it's likely I can clean this up somewhat.
        a = sorted([self, other], key=lambda n: n.start)
        a, b = a[0], a[1]
        return a.end >= b.start


def parse_input(filename: str):
    regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    elf_pairs = []
    with open(filename, "r") as file:
        for line in file:
            match = regex.match(line.strip())
            assign = ElfPair(
                SectionAssignment(int(match[1]), int(match[2])),
                SectionAssignment(int(match[3]), int(match[4]))
            )
            elf_pairs.append(assign)
    return elf_pairs


def main(input_filename: str):
    start_time = time.time()
    stuff = parse_input(input_filename)

    part1_start = time.time()
    total = 0
    for pair in stuff:
        total += int(pair.elf1.either_contains(pair.elf2))
    print(f"Part 1: {total} elves fully overlap their partner's assignment.")

    part2_start = time.time()
    total = 0
    for pair in stuff:
        total += int(pair.elf1.overlaps(pair.elf2))
    print(f"Part 2: {total} elves have overlap with their partner's assignment.")

    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")
    return


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day04.txt")

    run_main()
