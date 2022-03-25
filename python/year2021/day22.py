import time
import os
import collections
import re


Point = collections.namedtuple("Point", ["x", "y", "z"])
Instruction = collections.namedtuple("Instruction", ["value", "cube"])


class Cube:
    def __init__(self, corner1: Point, corner2: Point):
        self.c1: Point = corner1
        self.c2: Point = corner2

    def __repr__(self):
        return f"Cube: {self.c1.x, self.c1.y, self.c1.z}, {self.c2.x, self.c2.y, self.c2.z};"

    def is_valid(self) -> bool:
        return (self.c1.x < self.c2.x) and (self.c1.y < self.c2.y) and (self.c1.z < self.c2.z)

    @property
    def volume(self):
        return (self.c2.x - self.c1.x) * (self.c2.y - self.c1.y) * (self.c2.z - self.c1.z)


def get_overlap(a: Cube, b: Cube) -> Cube or None:
    overlap = Cube(Point(max(a.c1.x, b.c1.x), max(a.c1.y, b.c1.y), max(a.c1.z, b.c1.z)),
                   Point(min(a.c2.x, b.c2.x), min(a.c2.y, b.c2.y), min(a.c2.z, b.c2.z)))
    return overlap if overlap.is_valid() else None


def parse_input(filename: str) -> list[Instruction]:
    regex = re.compile(r"(on|off) x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)")
    instructions = []
    with open(filename, "r") as file:
        for line in file:
            if match := regex.search(line):
                value = match[1] == "on"
                pt1 = Point(int(match[2]), int(match[4]), int(match[6]))
                pt2 = Point(int(match[3]), int(match[5]), int(match[7]))
                assert pt1 == Point(min(pt1.x, pt2.x), min(pt1.y, pt2.y), min(pt1.z, pt2.z))
                assert pt2 == Point(max(pt1.x, pt2.x), max(pt1.y, pt2.y), max(pt1.z, pt2.z))
                # We add 1 to pt2's coordinates because of the grid system used to define cubes in the input file,
                # but what we want is the corner. A 1x1x1 cube with the first corner at 10,10,10 has the other corner
                # at 11,11,11, but we'll have x=10..10,y=10..10,z=10..10, so we have to add one to correct for this.
                pt2 = Point(pt2.x + 1, pt2.y + 1, pt2.z + 1)
                cube = Cube(pt1, pt2)
                instructions.append(Instruction(value, cube))
            else:
                # Complain if the assumption regarding the order of inputs is violated so those values aren't just
                # silently discarded.
                assert False, f"Error reading line: {line} -- are the coordinates out of order?"
    return instructions


def run_instructions_part_1(instructions: list[Instruction]):
    p1_instructions = []
    region = Cube(Point(-50, -50, -50), Point(51, 51, 51))
    for instruction in instructions:
        if (overlapping := get_overlap(region, instruction.cube)) is not None:
            p1_instructions.append(Instruction(instruction.value, overlapping))
    return run_instructions_reverse(p1_instructions)


def run_instructions_reverse(instructions: list[Instruction]):
    def check_overlaps(instructs, current, volume, depth):
        for instruction in instructs:
            if instruction.value:
                overlaps = []
                for cube in current:
                    if (overlapping := get_overlap(cube, instruction.cube)) is not None:
                        overlaps.append(Instruction(True, overlapping))
                temp = check_overlaps(overlaps, [], 0, depth + 1)
                dv = instruction.cube.volume - temp
                volume += dv
            current.append(instruction.cube)
        return max(0, volume)
    return check_overlaps(reversed(instructions), [], 0, 0)


def main(input_filename: str):
    start_time = time.time()
    instructions = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: {run_instructions_part_1(instructions)} lit cubes")
    # Proper results:
    # 607573 for real input
    part2_start = time.time()
    print(f"Part 2: {run_instructions_reverse(instructions)} lit cubes")
    # Proper results:
    # 1267133912086024 for real input
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day22.txt")
