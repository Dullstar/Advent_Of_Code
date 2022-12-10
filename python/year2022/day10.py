import time
import os
import enum
from collections import namedtuple


class Opcode(enum.Enum):
    noop = enum.auto()
    addx = enum.auto()


Instruction = namedtuple("Instruction", "opcode val")


class CPU:
    def __init__(self, instructions):
        self.cycle = 0
        self.instructions = instructions
        self.program_counter = -1
        self._current_instr_cycle = 0
        self.x = 1
        self.end = False
        self.advance_program_counter()
        assert self._current_instr_cycle != 0  # should have been updated by advance_program_counter

    # TODO: I'm like pretty sure they added a match/case thing to Python at some point that would probably be good here
    # but I think I'm going to complete the solution without it first particularly as the Python installation on this
    # machine does not auto update so I don't even know if I have access to it.
    def do_cycle(self):

        self.cycle += 1
        self._current_instr_cycle -= 1
        assert self._current_instr_cycle >= 0, f"Problem at cycle: {self.cycle}"
        # print(f"instruction cycle: {self.instructions[self.program_counter]}: {self._current_instr_cycle}")
        if (instr := self.instructions[self.program_counter]).opcode == Opcode.addx and self._current_instr_cycle == 0:
            self.x += instr.val
            # print(f"x += {instr.val} -> x = {self.x}")
        if self._current_instr_cycle == 0:
            self.advance_program_counter()

    def advance_program_counter(self):
        # Compare some other methods later; a dictionary would be convenient, but would it perform?
        # A list would also be an option, but it feels like a potential maintainence nightmare... but it's AoC so
        # there's not really maintanence to do.
        self.program_counter += 1
        if self.program_counter >= len(self.instructions):
            self.end = True
            return
        if (instr := self.instructions[self.program_counter]).opcode == Opcode.noop:
            self._current_instr_cycle = 1
        elif instr.opcode == Opcode.addx:
            self._current_instr_cycle = 2
        else:
            assert False, f"wut? {instr}"

    def run_program(self):
        samples = []
        output = ""
        while not self.end:
            if (x := self.cycle % 40) == 0 and output != "":
                output += "\n"
            output += "█" if self.x <= x + 1 <= self.x + 2 else " "
            self.do_cycle()
            # I don't know WHY starting at 19 and not 20 gives the right answer, but it does.
            if self.cycle in range(19, 221, 40):
                samples.append(self.x * (self.cycle + 1))
            # The off-by-one errors corrected here were experimentally determined through the magic of debugging.
        return sum(samples), output


def parse_input(filename: str):
    instructions = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip().split()
            instructions.append(Instruction(Opcode[line[0]], int(line[1]) if len(line) == 2 else None))
    # print(instructions)
    return CPU(instructions)


def main(input_filename: str):
    start_time = time.time()
    cpu = parse_input(input_filename)
    part1_start = time.time()
    pt1, pt2 = cpu.run_program()
    end_time = time.time()
    print(f"Part 1: Signal strength sum: {pt1}")
    print(f"Part 2:\n{pt2}")
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1 + Part 2: {(end_time - part1_start) * 1000:.2f} ms (evaluation is combined today)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day10.txt")


    run_main()
