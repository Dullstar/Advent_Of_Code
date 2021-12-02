import time
import os


class Instruction:
    def __init__(self, direction: str, distance: int):
        self.direction = direction
        self.distance = distance


class Position:
    def __init__(self, horizontal_pos: int, depth: int, aim: int):
        self.horizontal_pos = horizontal_pos
        self.depth = depth
        self.aim = aim

    def process_instruction(self, cmd: Instruction) -> None:
        # Handles both part 1 and part 2; see main for notes on how aim and depth are handled to allow this.
        if cmd.direction == "forward":
            self.horizontal_pos += cmd.distance
            self.depth += (cmd.distance * self.aim)
        elif cmd.direction == "down":
            self.aim += cmd.distance
        elif cmd.direction == "up":
            self.aim -= cmd.distance

    def run_course(self, instructions: list[Instruction]) -> None:
        for instruction in instructions:
            self.process_instruction(instruction)


def parse_input(filename: str) -> list[Instruction]:
    instructions = []
    with open(filename, "r") as file:
        for line in file:
            line = line.split()
            instructions.append(Instruction(line[0], int(line[1])))
    return instructions


def main(input_filename: str):
    start_time = time.time()
    instructions = parse_input(input_filename)
    part1_start = time.time()
    submarine_pos = Position(0, 0, 0)
    submarine_pos.run_course(instructions)
    # This part deserves some explanation: The aim variable in part 2 is set the exact same way that the depth variable
    # is for part 1, and the effect of horizontal distance is also the same in part 1 and part 2. Thus, depth refers
    # to part 2, and refer to aim when we want the depth in part 1. This allows considerable code de-duplication as well
    # as faster runtime since we can solve Part 1 using information we needed anyway to solve Part 2.
    print(f"Part 1: Horizontal position: {submarine_pos.horizontal_pos}; Depth: {submarine_pos.aim}; "
          f"Product: {submarine_pos.horizontal_pos * submarine_pos.aim}")
    print(f"Part 2: Horizontal position: {submarine_pos.horizontal_pos}; Depth: {submarine_pos.depth}; "
          f"Aim: {submarine_pos.aim}; Product (excludes aim): {submarine_pos.horizontal_pos * submarine_pos.depth}")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1 + Part 2: {(end_time - part1_start) * 1000:.2f} ms (evaluation is combined today)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day02.txt")
