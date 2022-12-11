import time
import os
import re
import enum
from functools import reduce
from copy import deepcopy


class OperationType(enum.Enum):
    Add = enum.auto()
    Mult = enum.auto()
    Square = enum.auto()


class Operation:
    parsing_regex = re.compile(r"old ([*+]) (\d+|old)")

    def __init__(self, string_form):
        self.type = None
        self.value = None
        match = self.parsing_regex.match(string_form)
        assert match is not None
        if match[2] == "old":
            if match[1] == "+":
                self.type = OperationType.Mult
                self.value = 2
            elif match[1] == "*":
                self.type = OperationType.Square
                self.value = 2
        elif match[1] == "+":
            self.type = OperationType.Add
            self.value = int(match[2])
        elif match[1] == "*":
            self.type = OperationType.Mult
            self.value = int(match[2])
        assert self.type is not None
        assert self.value is not None

    def apply(self, in_value: int):
        match self.type:
            case OperationType.Add:
                return in_value + self.value
            case OperationType.Mult:
                return in_value * self.value
            case OperationType.Square:
                return in_value ** 2
            case _:
                assert False


class Monkey:
    def __init__(self, inventory, operation, test, true_target, false_target):
        self.inventory = inventory
        self.operation = operation
        self.test = test
        self.true_target = true_target
        self.false_target = false_target
        self.inspections = 0

    def take_turn(self, monkeys, part1=True, part2magicnumber=1):
        self.inspections += len(self.inventory)
        for item in self.inventory:
            item = self.operation.apply(item)
            if part1:
                item //= 3
            else:
                item %= part2magicnumber
            if item % self.test == 0:
                monkeys[self.true_target].inventory.append(item)
            else:
                monkeys[self.false_target].inventory.append(item)
        self.inventory = []


def do_rounds(monkeys: list[Monkey], rounds, part1):
    if not part1:
        part2magicnumber = reduce(lambda x, y: x * y, [i for i in map(lambda n: n.test, monkeys)])
    else:
        part2magicnumber = 1
    for i in range(rounds):
        for monkey in monkeys:
            monkey.take_turn(monkeys, part1, part2magicnumber)
    results = [i for i in map(lambda n: n.inspections, monkeys)]
    results.sort(reverse=True)
    return results[0] * results[1]


def parse_input(filename: str):
    regex = r"Monkey (\d+):\s*Starting items: (.+)\n\s*Operation: new = (.*)\n\s*Test: divisible by (\d+)\s*If true: " \
            r"throw to monkey (\d)\s*If false: throw to monkey (\d)"
    regex = re.compile(regex)
    monkeys = []
    with open(filename, "r") as file:
        monkey_strings = file.read().strip().split("\n\n")
        for i, string in enumerate(monkey_strings):
            match = regex.match(string)
            assert match is not None
            assert i == int(match[1])
            monkeys.append(Monkey(
                [int(item) for item in match[2].split(", ")],
                Operation(match[3]),
                int(match[4]),
                int(match[5]),
                int(match[6])
            ))
    return monkeys


def main(input_filename: str):
    start_time = time.time()
    monkeys = parse_input(input_filename)
    pt2monkeys = deepcopy(monkeys)  # It's just easier than resetting to the initial state.
    part1_start = time.time()
    print(f"Part 1: Monkey business score: {do_rounds(monkeys, 20, part1=True)}")
    part2_start = time.time()
    print(f"Part 2: Monkey business score: {do_rounds(pt2monkeys, 10000, part1=False)}")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day11.txt")

    run_main()
