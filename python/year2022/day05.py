import time
import os
from copy import deepcopy
from collections import namedtuple

Move = namedtuple("Move", ["quantity", "start", "end"])


class Layout:
    def __init__(self, stacks: list[list[str]]):
        self.stacks = stacks
        self._init_state = deepcopy(stacks)  # Used for resetting.

    def reset(self):
        self.stacks = deepcopy(self._init_state)

    def run_move(self, move: Move):
        for _ in range(move.quantity):
            self.stacks[move.end].append(self.stacks[move.start].pop())

    def run_move_2(self, move: Move):
        crate_buffer = []
        for _ in range(move.quantity):
            crate_buffer.append(self.stacks[move.start].pop())
        for item in reversed(crate_buffer):
            self.stacks[move.end].append(item)

    def get_top_crates(self) -> str:
        output = ""
        for stack in self.stacks:
            output += stack[-1]
        return output


def parse_input(filename: str) -> (Layout, list[Move]):
    def parse_layout(contents: str):
        stacks = []
        first = True
        for line in contents.split("\n")[:-1]:  # We remove the number labels since they're in order and thus not needed
            # Desired indices: 1..., 5..., 9...
            for pos, index in enumerate(range(1, len(line), 4)):
                if first:
                    stacks.append([])
                if line[index] != " ":
                    stacks[pos].append(line[index])  # This won't be in the right order...
            first = False
        for stack in stacks:
            stack.reverse()  # ...but we can reverse it once we're done to fix that!
        return Layout(stacks)

    def parse_moves(contents: str):
        moves = []
        for line in contents.strip().split("\n"):
            line = line.split(" ")
            # Split result: move[0] a[1] from[2] b[3] to[4] c[5]
            moves.append(Move(int(line[1]), int(line[3]) - 1, int(line[5]) - 1))  # -1 makes indexing more convenient
        return moves

    with open(filename, "r") as file:
        stuff = file.read().split("\n\n")
        return parse_layout(stuff[0]), parse_moves(stuff[1])


def main(input_filename: str):
    start_time = time.time()
    layout, moves = parse_input(input_filename)

    part1_start = time.time()
    for move in moves:
        layout.run_move(move)
    print(f"Part 1: Top crates are \"{layout.get_top_crates()}\"")

    part2_start = time.time()
    layout.reset()
    for move in moves:
        layout.run_move_2(move)
    print(f"Part 2: Top crates are \"{layout.get_top_crates()}\"")

    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day05.txt")

    run_main()
