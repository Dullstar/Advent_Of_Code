import time
import os
import enum
import re


class OperationType(enum.Enum):
    add = enum.auto()
    sub = enum.auto()
    mul = enum.auto()
    div = enum.auto()

    @staticmethod
    def from_str(string: str):
        match string:
            case "+":
                return OperationType.add
            case "-":
                return OperationType.sub
            case "*":
                return OperationType.mul
            case "/":
                return OperationType.div
        raise KeyError(f"{string} is not a possible value for OperationType")


class OperationMonkey:
    def __init__(self, first, second, operation):
        self.first: int or str = first
        self.second: int or str = second
        self.operation: OperationType = operation

    def process(self, monkeys):
        self.first = self.lookup_monkey(monkeys, self.first)
        self.second = self.lookup_monkey(monkeys, self.second)
        if type(self.first) == int and type(self.second) == int:
            match self.operation:
                case OperationType.add:
                    return self.first + self.second
                case OperationType.sub:
                    return self.first - self.second
                case OperationType.mul:
                    return self.first * self.second
                case OperationType.div:
                    return self.first // self.second
        return self

    @staticmethod
    def lookup_monkey(monkeys, monkey_id):
        if type(monkey_id) == str and type(monkey_val := monkeys[monkey_id]) == int:
            return monkey_val
        return monkey_id

    def __repr__(self):
        match self.operation:
            case OperationType.add:
                opstr = "+"
            case OperationType.sub:
                opstr = "-"
            case OperationType.mul:
                opstr = "*"
            case OperationType.div:
                opstr = "/"
            case _:
                assert False
        return f"{self.first} {opstr} {self.second}"


def process_monkeys_pt1(monkeys: dict[str: int or OperationMonkey]):
    while type(monkeys["root"]) != int:
        process_monkeys_pt1_step(monkeys)
    return monkeys["root"]


def process_monkeys_pt1_step(monkeys: dict[str: int or OperationMonkey]):
    # new_monkeys = dict()
    unfinished = False
    for monkey_id, monkey in monkeys.items():
        if type(monkey) == OperationMonkey:
            new_monkey = monkey.process(monkeys)
            if type(new_monkey) == int:
                monkeys[monkey_id] = new_monkey
            else:
                unfinished = True
    for monkey_id, monkey in monkeys.items():
        print(f"{monkey_id}: {monkey}")
    print()
    return unfinished


def process_monkeys_pt2(monkeys: dict[str: int or OperationMonkey]):
    del monkeys["root"]
    del monkeys["humn"]
    print("SQUEAL")
    while process_monkeys_pt2_step(monkeys):
        pass
        input()
    return monkeys["root"]


def process_monkeys_pt2_step(monkeys: dict[str: int or OperationMonkey]):
    print("KITTY")
    # new_monkeys = dict()
    unfinished = False
    for monkey_id, monkey in monkeys.items():
        if type(monkey) == OperationMonkey:
            new_monkey = monkey.process(monkeys)
            if type(new_monkey) == int:
                monkeys[monkey_id] = new_monkey
            else:
                unfinished = True
    for monkey_id, monkey in monkeys.items():
        print(f"{monkey_id}: {monkey}")
    print()
    return unfinished


def parse_input(filename: str):
    monkeys = dict()
    opmonkey_re = re.compile(r"(\w+): (\w+) ([+\-\*/]) (\w+)")
    int_re = re.compile(r"(\w+): (\d+)")
    with open(filename, "r") as file:
        for line in file:
            if (match := opmonkey_re.match(line)) is not None:
                monkeys[match[1]] = OperationMonkey(match[2], match[4], OperationType.from_str(match[3]))
            elif (match := int_re.match(line)) is not None:
                monkeys[match[1]] = int(match[2])
            else:
                assert False
    return monkeys


def main(input_filename: str):
    monkeys = parse_input("test_input.txt")
    for monkey_id, monkey in monkeys.items():
        print(f"{monkey_id}: {monkey}")
    print()
    print(f"Part 1: {process_monkeys_pt1(monkeys)}")

    monkeys = parse_input("test_input.txt")
    for monkey_id, monkey in monkeys.items():
        print(f"{monkey_id}: {monkey}")
    print()
    print(f"Part 2: {process_monkeys_pt2(monkeys)}")
    return -1


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day21.txt")

    run_main()
