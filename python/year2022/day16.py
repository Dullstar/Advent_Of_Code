import time
import os
import re
from collections import namedtuple


# open = bool
Move = namedtuple("Move", "dest open")


class Valve:
    def __init__(self, label, flow_rate, connections):
        self.label = label
        self.flow_rate = flow_rate
        self.connections = connections

    def __repr__(self):
        return f"Valve {self.label}: Flow rate {self.flow_rate}, connections {self.connections}"


def parse_input(filename: str):
    valves = dict()
    with open(filename, "r") as file:
        regex = re.compile(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
        for line in file:
            match = regex.match(line)
            assert match is not None
            valves[match[1]] = Valve(match[1], int(match[2]), match[3].split(", "))
    return valves


def solve_part_1(valves):
    start = "AA"


def main(input_filename: str):
    return -1
    valves = parse_input("test_input.txt")
    print(valves)


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day16.txt")

    run_main()
