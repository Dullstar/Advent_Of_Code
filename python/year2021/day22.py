import time
import os
import collections
import re


Point = collections.namedtuple("Point", ["x", "y", "z"])
Instruction = collections.namedtuple("Instruction", ["value", "cuboid"])


class Cuboid:
    def __init__(self, corner1: Point, corner2: Point):
        self.c1: Point = corner1
        self.c2: Point = corner2

    def __repr__(self):
        return f"Cuboid: {self.c1.x, self.c1.y, self.c1.z}, {self.c2.x, self.c2.y, self.c2.z};"

    def is_valid(self) -> bool:
        return (self.c1.x < self.c2.x) and (self.c1.y < self.c2.y) and (self.c1.z < self.c2.z)

    @property
    def volume(self):
        return (self.c2.x - self.c1.x) * (self.c2.y - self.c1.y) * (self.c2.z - self.c1.z)


def get_overlap(a: Cuboid, b: Cuboid) -> Cuboid or None:
    # I'm not sure about a good way to explain where this formula comes from other than to draw it out with squares
    # (it'll extend out to 3 dimensions trivially), but if we do this process, and we get a cuboid that fits the
    # format that Cuboid.is_valid() expects in order for it to return True, then it's the cuboid that describes where
    # the overlap occurs, while if it returns False, then that tells us there's no overlap and we can safely discard
    # the cuboid we found.
    overlap = Cuboid(Point(max(a.c1.x, b.c1.x), max(a.c1.y, b.c1.y), max(a.c1.z, b.c1.z)),
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
                assert pt1 == Point(min(pt1.x, pt2.x), min(pt1.y, pt2.y), min(pt1.z, pt2.z)), \
                    "Input data ordering doesn't comply with expected min..max format"
                assert pt2 == Point(max(pt1.x, pt2.x), max(pt1.y, pt2.y), max(pt1.z, pt2.z)), \
                    "Input data ordering doesn't comply with expected min..max format"
                # We add 1 to pt2's coordinates because of the grid system used to define cuboids in the input file,
                # but what we want is the corner. A 1x1x1 cuboid with the first corner at 10,10,10 has the other corner
                # at 11,11,11, but we'll have x=10..10,y=10..10,z=10..10, so we have to add one to correct for this.
                pt2 = Point(pt2.x + 1, pt2.y + 1, pt2.z + 1)
                cuboid = Cuboid(pt1, pt2)
                instructions.append(Instruction(value, cuboid))
            else:
                # Complain if the assumption regarding the order of inputs is violated so those values aren't just
                # silently discarded.
                assert False, f"Error reading line: {line} -- are the coordinates out of order?"
    return instructions


def run_instructions_part_1(instructions: list[Instruction]):
    p1_instructions = []
    region = Cuboid(Point(-50, -50, -50), Point(51, 51, 51))
    # Get cuboids fitting part 1's criteria by grabbing the section of each cuboid that overlaps the region of interest.
    for instruction in instructions:
        if (overlapping := get_overlap(region, instruction.cuboid)) is not None:
            p1_instructions.append(Instruction(instruction.value, overlapping))
    return run_instructions(p1_instructions)


def run_instructions(instructions: list[Instruction]):
    placed = []
    volume = 0
    # Reversing the list makes it so we don't have to treat OFF values any differently from ON values, except their
    # volume doesn't change the total when they're first encountered: the last cuboid always contributes its full
    # volume to the final volume, then each subsequent ON cuboid contributes whatever portion of its volume doesn't
    # overlap with any other cuboids. Thus, both ON and OFF cuboids cut into the contributions by earlier cuboids
    # (the ones we visit last) in identical ways. If we went forward, we'd have to keep closer track of ON vs. OFF
    # when determining how much extra volume each additional cuboid contributes.
    #
    # In the special case where all the cuboids are ON (well, probably OFF too, but that doesn't actually happen),
    # then it doesn't make a difference. This comes up when we determine how much to subtract from a given cuboid's
    # volume later.
    for instruction in reversed(instructions):
        # We only need to add the volume if the cuboid is ON, i.e. instruction.value == True; otherwise we don't
        # need to do anything.
        if instruction.value:
            overlaps = []
            for cuboid in placed:
                if (overlapping := get_overlap(cuboid, instruction.cuboid)) is not None:
                    # Since we'll be checking these overlaps for more overlaps to get the volume of overlap,
                    # we want to always treat the result of get_overlap as ON. If it were OFF we'd fail to cut into
                    # the volume.
                    overlaps.append(Instruction(True, overlapping))
            # The overlaps can be overlapping themselves, so we'll need to handle that to figure out
            # exactly how much we should be subtracting from the volume.
            volume += instruction.cuboid.volume - run_instructions(overlaps)
        # The cuboid still needs to be remembered either way because both ON and OFF cuboids already placed
        # will both mask pieces from whatever cuboids are behind them.
        placed.append(instruction.cuboid)
    assert volume >= 0, "Negative volume shouldn't happen"
    return volume


def main(input_filename: str):
    start_time = time.time()
    instructions = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: {run_instructions_part_1(instructions)} lit cubes")
    part2_start = time.time()
    print(f"Part 2: {run_instructions(instructions)} lit cubes")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day22.txt")
