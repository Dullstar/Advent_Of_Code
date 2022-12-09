import time
import os
from collections import namedtuple
import enum


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point x={self.x}, y={self.y}"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def direction_only(self):
        new_x = self.x // abs(self.x) if self.x != 0 else 0
        new_y = self.y // abs(self.y) if self.y != 0 else 0
        return Point(new_x, new_y)


class Direction(enum.Enum):
    Up = Point(0, -1)
    Down = Point(0, 1)
    Left = Point(-1, 0)
    Right = Point(1, 0)
    DUpLeft = Point(-1, -1)
    DUpRight = Point(1, -1)
    DDownLeft = Point(-1, 1)
    DDownRight = Point(1, 1)


class DirectionLists:
    NonDiagonal = [Direction.Up, Direction.Down, Direction.Left, Direction.Right]
    Diagonal = [Direction.DUpLeft, Direction.DUpRight, Direction.DDownRight, Direction.DDownLeft]
    All = [Direction.Up, Direction.Down, Direction.Left, Direction.Right,
           Direction.DUpLeft, Direction.DUpRight, Direction.DDownRight, Direction.DDownLeft]


Step = namedtuple("Step", "direction quantity")


class Rope:
    NO_MOVE = 1  # arbitrary value, used by move_tail to signal no movement

    def __init__(self, head: Point, tail: Point):
        self.head = head
        self.tail = tail

    def check_tail(self):
        for direction in DirectionLists.All:
            if self.head + direction.value == self.tail:
                return True
        return self.head == self.tail

    def move_tail(self):
        if self.check_tail():
            # print("Did not move the tail.")
            return self.NO_MOVE
        for direction in DirectionLists.NonDiagonal:
            # since we only need to multiply by 2, no reason to define scalar mult.
            double = direction.value + direction.value
            if self.tail + double == self.head:
                self.tail += direction.value
                return
        change = (self.head - self.tail).direction_only()
        self.tail += change


class CursedRope:
    def __init__(self, depth=0):
        self.child = CursedRope(depth+1) if depth < 8 else None
        self.depth = depth  # For debugging purposes only
        self.rope = Rope(Point(0, 0), Point(0, 0))

    def move_tail(self):
        # If this segment doesn't move, there's no chance that the next one can move, and so on, so forth,
        # so we can stop if that happens.
        if self.rope.move_tail() != Rope.NO_MOVE and self.child is not None:
            self.child.rope.head = self.rope.tail
            self.child.move_tail()

    def get_true_tail_pos(self):
        if self.child is not None:
            return self.child.get_true_tail_pos()
        return self.rope.tail

    def __repr__(self):
        output = f"CR: depth {self.depth}, rope: {self.rope.head}, {self.rope.tail}\n"
        if self.child is not None:
            output += self.child.__repr__()
        return output


def parse_input(filename: str):
    dir_dict = {"U": Direction.Up, "D": Direction.Down, "L": Direction.Left, "R": Direction.Right}
    steps = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip().split()
            steps.append(Step(dir_dict[line[0]], int(line[1])))
    return steps


def move_knot(grid: set, step: Step, rope: Rope):
    for _ in range(step.quantity):
        # print(step.direction.value)
        rope.head += step.direction.value
        rope.move_tail()
        grid.add(rope.tail)


def move_cursed_knot(grid: set, step: Step, rope: CursedRope):
    for _ in range(step.quantity):
        rope.rope.head += step.direction.value
        rope.move_tail()
        grid.add(rope.get_true_tail_pos())


def main(input_filename: str):
    start_time = time.time()
    steps = parse_input(input_filename)
    grid: set = {Point(0, 0)}
    rope = Rope(Point(0, 0), Point(0, 0))
    part1_start = time.time()
    for step in steps:
        move_knot(grid, step, rope)
    print(f"Part 1: Tail visits {len(grid)} locations")
    part2_start = time.time()
    grid: set = {Point(0, 0)}
    cursed_rope = CursedRope()
    for step in steps:
        move_cursed_knot(grid, step, cursed_rope)
    print(f"Part 2: Tail visits {len(grid)} locations")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day09.txt")

    run_main()
