import time
import os
import collections
import itertools
import re


Point = collections.namedtuple("Point", ["x", "y", "z"])
Instruction = collections.namedtuple("Instruction", ["value", "cube"])


class Cube:
    def __init__(self, corner1, corner2):
        self.c1: Point = corner1
        self.c2: Point = corner2

    def __repr__(self):
        return f"Cube: {self.c1.x, self.c1.y, self.c1.z}, {self.c2.x, self.c2.y, self.c2.z};"

    @property
    def area(self):
        return (self.c2.x - self.c1.x + 1) * (self.c2.y - self.c1.y + 1) * (self.c2.z - self.c1.z + 1)

    def overlap_cube(self, other):
        # Credit to reddit user u/alykzandr; see run_instructions_pt2 for more details
        max_c1 = Point(max(self.c1.x, other.c1.x), max(self.c1.y, other.c1.y), max(self.c1.z, other.c1.z))
        min_c2 = Point(min(self.c2.x, other.c2.x), min(self.c2.y, other.c2.y), min(self.c2.z, other.c2.z))
        if (min_c2.x - max_c1.x >= 0) and (min_c2.y - max_c1.y >= 0) and (min_c2.z - max_c1.z >= 0):
            return Cube(max_c1, min_c2)


class Core:
    def __init__(self):
        self.layout = collections.defaultdict(lambda: False)

    def add_or_remove_cubes(self, instruction: Instruction):
        for x, y, z in itertools.product(
                self.make_range(instruction.cube.c1.x, instruction.cube.c2.x),
                self.make_range(instruction.cube.c1.y, instruction.cube.c2.y),
                self.make_range(instruction.cube.c1.z, instruction.cube.c2.z)):
            self.layout[Point(x, y, z)] = instruction.value

    @staticmethod
    def make_range(value1, value2):
        # Probably room for improvement
        if value1 > 50 and value2 > 50:
            return range(0)
        if value1 < -50 and value2 < -50:
            return range(0)
        if value1 < -50:
            value1 = -50
        elif value1 > 50:
            value1 = 50
        if value2 < -50:
            value2 = -50
        elif value2 > 50:
            value2 = 50
        return range(value1, value2 + 1)

    def count_cubes(self):
        total = 0
        for point in self.layout:
            total += self.layout[point]
        return total

    def run_instructions(self, instructions: list[Instruction]):
        for i, instruction in enumerate(instructions):
            # print(f"Running instruction {i + 1} of {len(instructions)}")
            self.add_or_remove_cubes(instruction)
        return self.count_cubes()


def run_instructions_pt2(instructions: list[Instruction]):
    # See https://www.reddit.com/r/adventofcode/comments/rmbp88/2021_day_22_how_to_think_about_the_problem/hpmeisa/
    # (links to https://pastebin.com/13WiZbLk) for the code this is adapted from (i.e. basically just rewritten in
    # my own style, with no actual changes to how it behaves). Solution credit: reddit user u/alykzandr
    counted = []
    lit = 0
    i = 0
    for instruction in reversed(instructions):
        i += 1
        if instruction.value:
            overlaps = []
            for overlap_cube in [cube.overlap_cube(instruction.cube) for cube in counted]:
                if overlap_cube:
                    overlaps.append(Instruction(True, overlap_cube))
            lit += instruction.cube.area
            lit -= run_instructions_pt2(overlaps)
        counted.append(instruction.cube)
    return lit


def parse_input(filename: str) -> list[Instruction]:
    regex = re.compile(r"(on|off) x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)")
    instructions = []
    with open(filename, "r") as file:
        for line in file:
            if match := regex.search(line):
                value = match[1] == "on"
                corner1 = Point(int(match[2]), int(match[4]), int(match[6]))
                corner2 = Point(int(match[3]), int(match[5]), int(match[7]))
                instructions.append(Instruction(value, Cube(corner1, corner2)))
    return instructions


def main(input_filename: str):
    start_time = time.time()
    instructions = parse_input(input_filename)
    part1_start = time.time()
    core = Core()
    print(f"Part 1: {core.run_instructions(instructions)} lit cubes")
    part2_start = time.time()
    print(f"Part 2: {run_instructions_pt2(instructions)} lit cubes")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day22.txt")
