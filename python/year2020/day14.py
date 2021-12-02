import time
import os
import enum
import re


class MutableString:
    def __init__(self, string: str):
        self._contents = [char for char in string]

    @property
    def str(self):
        string = ""
        for char in self._contents:
            string += char
        return string

    @str.setter
    def str(self, string):
        self.__init__(string)

    # Minimal for this problem. If expanded to a full implementation, we'd probably want to implement much of this:
    # https://docs.python.org/3/reference/datamodel.html#emulating-container-types
    def __getitem__(self, key):
        return self._contents[key]

    def __setitem__(self, key, value):
        self._contents[key] = value


class Command(enum.Enum):
    CHANGE_MASK = enum.auto()
    WRITE = enum.auto()


class Instruction:
    def __init__(self, command: Command, address: int, value: str or int):
        assert((command == Command.CHANGE_MASK and type(value) == str)
               or (command == Command.WRITE and type(value) == int and address >= 0))

        self.command = command
        self.address = address
        self.value = value

    # for testing purposes
    @property
    def to_string(self):
        if self.command == Command.CHANGE_MASK:
            return f"mask = {self.value}"
        elif self.command == Command.WRITE:
            return f"mem[{self.address}] = {self.value}"


class Mask:
    # can turn off eval_replacements to save some work if we won't be using this mask with
    # float_write
    def __init__(self, value: str, eval_replacements: bool = True):
        self.raw_mask = value
        self.x_to_ones = self._replace_x(value, "1")
        self.x_to_zeroes = self._replace_x(value, "0")
        self.x_locations = []
        self.combinations = []
        self.eval_replacements = eval_replacements  # stored for use in asserts
        if eval_replacements:
            for i, char in enumerate(self.raw_mask):
                if char == "X":
                    self.x_locations.append(i)
            combo = None
            new_mask_string = MutableString("".zfill(len(self.raw_mask)))
            while combo := self.float_mask_advance(combo):
                for i, x in enumerate(self.x_locations):
                    char = combo[i]
                    new_mask_string[x] = char
                self.combinations.append(Mask(new_mask_string.str, False))

    @staticmethod
    def _replace_x(value: str, replace_with: str):
        output = ""
        for char in value:
            if char == "X":
                char = replace_with
            output += char
        return int(output, 2)

    def float_mask_advance(self, current: str or None):
        if current is None:
            return "0" * len(self.x_locations)

        target = int("1" * len(current), 2)
        current = int(current, 2)
        if current == target:
            return False
        else:
            current += 1
        return str(bin(current))[2:].zfill(len(self.x_locations))  # chop off the 0b prefix

    def apply_mask_to_value(self, value: int):
        value &= self.x_to_ones
        value |= self.x_to_zeroes
        return value

    def apply_mask_to_address(self, address: int, x_to_one_mask: int):
        assert self.raw_mask.count("X") == 0
        mask = ~int(self.raw_mask, 2)  # bitwise stuff going on
        address |= x_to_one_mask
        address &= mask
        return address


class Memory:
    def __init__(self):
        self.contents = {}
        self._mask = Mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", False)

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, value: str):
        self._mask = Mask(value)

    def reset_memory(self):
        self.__init__()

    def write(self, address: int, value: int, mask: Mask = None):
        if mask is not None:
            value = self.mask.apply_mask_to_value(value)
        self.contents[address] = value

    def float_write(self, address: int, value: int, mask: Mask):
        assert mask.eval_replacements
        for new_mask in mask.combinations:
            self.write(new_mask.apply_mask_to_address(address, mask.x_to_ones), value, None)

    def sum_contents(self):
        return sum(self.contents.values())


def parse_input(filename: str):
    with open(filename, "r") as file:
        lines = [line.strip() for line in file]

    instructions = []
    for line in lines:
        if line[1] == "a":  # minimum amount of stuff we can check to distinguish mask and mem commands
            cmd = Command.CHANGE_MASK
            address = -1
            value = re.match(r"mask = (.*)", line).group(1)

        else:
            cmd = Command.WRITE
            match = re.match(r"mem\[([0-9]*)] = ([0-9]*)", line)
            address = int(match.group(1))
            value = int(match.group(2))

        instructions.append(Instruction(cmd, address, value))

    return instructions


def main(input_filename: str):
    start_time = time.time()
    instructions = parse_input(input_filename)
    memory = Memory()
    memory_version_2 = Memory()
    part1_start = time.time()
    for instruction in instructions:
        if instruction.command == Command.CHANGE_MASK:
            memory.mask = instruction.value
        elif instruction.command == Command.WRITE:
            memory.write(instruction.address, instruction.value, memory.mask)

    # This could be combined with the other loop, but then we can't easily measure part 1 vs. part 2
    part2_start = time.time()
    for instruction in instructions:
        if instruction.command == Command.CHANGE_MASK:
            memory_version_2.mask = instruction.value
        elif instruction.command == Command.WRITE:
            memory_version_2.float_write(instruction.address, instruction.value, memory_version_2.mask)

    end_time = time.time()
    print(f"Part 1: Sum of memory contents: {memory.sum_contents()}")
    print(f"Part 2: Sum of memory contents: {memory_version_2.sum_contents()}")

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2020/day14.txt")

    run_main()
