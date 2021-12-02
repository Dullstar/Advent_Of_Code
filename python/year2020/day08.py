import time
import os


class Instruction:
    def __init__(self, opcode: str, arg: int or str):
        self.arg = int(arg)
        self.opcode = opcode


class Console:
    def __init__(self):
        self.accumulator = 0
        self.program_counter = 0

    def acc(self, arg: int):
        self.accumulator += arg
        self.program_counter += 1

    def jmp(self, arg: int):
        self.program_counter += arg

    def nop(self):
        self.program_counter += 1

    def execute_command(self, instruction: Instruction):
        if instruction.opcode == "acc":
            self.acc(instruction.arg)
        elif instruction.opcode == "jmp":
            self.jmp(instruction.arg)
        elif instruction.opcode == "nop":
            self.nop()
        return self.program_counter


def parse_input(filename: str):
    code = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip().split()
            code.append(Instruction(line[0], line[1]))
    return code


def report(succeeded: bool, accumulator: int, program_counter: int):
    if succeeded:
        print(f"The accumulator was at {accumulator} when the program completed at program counter {program_counter}")
    else:
        print(f"The accumulator status was {accumulator} at program counter {program_counter}")
        print("at the moment an instruction first ran for the second time")


# This function isn't actually important to solve the problem, but I thought it would be a nice touch
# to be able to see what exactly is different between the original and the new one.
def report_change(original: Instruction, new: Instruction):
    print(f"    Original: {original.opcode}, {original.arg}")
    print(f"    New:      {new.opcode}, {new.arg}")


def run_code(code: list, suppress_fail: bool = False):
    visited = []
    console = Console()
    next_command = 0
    completed = False
    # Part 1
    while not completed:
        if next_command >= len(code):
            completed = True
        elif next_command in visited:
            break
        else:
            visited.append(next_command)
            next_command = console.execute_command(code[next_command])

    if completed or not suppress_fail:
        report(completed, console.accumulator, console.program_counter)
    return completed, console.accumulator, console.program_counter


def correct_code(code: list):
    new_code = code.copy()
    attempts = 0  # Output flavor
    for cmd in new_code:
        if cmd.opcode == "jmp":
            cmd.opcode = "nop"
            output = run_code(new_code, suppress_fail=True)
            if output[0]:
                report_change(Instruction("jmp", cmd.arg), cmd)
                print("    Attempts: ", attempts + 1)
                return output
            else:
                cmd.opcode = "jmp"  # put it back how we found it, since we're only allowed to change one.
                attempts += 1
        elif cmd.opcode == "nop":
            cmd.opcode = "jmp"
            output = run_code(new_code, suppress_fail=True)
            if output[0]:
                report_change(Instruction("nop", cmd.arg), cmd)
                print("    Attempts: ", attempts + 1)
                return output
            else:
                attempts += 1
                cmd.opcode = "nop"  # put it back how we found it, since we're only allowed to change one.

    # If we haven't returned yet, nothing was found.
    print("Failed to find possible fix.")
    return False, None, None


def main(input_filename: str):
    # The output on this might get reworked later. It made sense in the original standalone version, but now it's
    # a bit inconsistent with the others, particularly for adding part 1 and part 2 labels.
    start_time = time.time()
    code = parse_input(input_filename)
    print("Part 1: ", end="")
    part1_start = time.time()
    run_code(code)
    part2_start = time.time()
    print("Part 2: ", end="")
    correct_code(code)
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2020/day08.txt")
