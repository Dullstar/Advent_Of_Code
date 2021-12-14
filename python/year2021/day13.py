import time
import re
import os
import collections


class Point:  # can't use namedtuple, as it is immutable.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.y << 16 | self.x


Fold = collections.namedtuple("Fold", ["along_x", "value"])


class Paper:
    def __init__(self, points: list[Point], size_x: int, size_y: int, folds: list[Fold]):
        self.size_x = size_x
        self.size_y = size_y
        self.folds = folds
        self.points = points
        self.layout = None

    def __str__(self):
        if self.layout is None:
            self.generate_layout()
        x, y = 0, 0
        string = ""
        for item in self.layout:
            string += ("█" if item else " ")
            x += 1
            if x == self.size_x:
                string += "\n"
                x = 0
                y += 1
        return string

    def generate_layout(self):
        self.layout = [False] * (self.size_x * self.size_y)
        for point in self.points:
            self.layout[point.x + (point.y * self.size_x)] = True

    def fold(self, fold):
        self.layout = None  # invalidate current layout
        for point in self.points:
            if fold.along_x and fold.value < point.x:
                point.x = -point.x + (2 * fold.value)
                self.size_x = fold.value
            elif (not fold.along_x) and fold.value < point.y:
                point.y = -point.y + (2 * fold.value)
                self.size_y = fold.value
        self.points = list(set(self.points))
        return len(self.points)

    def fold_all(self):
        for fold in self.folds:
            self.fold(fold)

        self.layout = None
        print(self)


def parse_input(filename: str):
    with open(filename, "r") as file:
        contents = file.read()
    contents = contents.strip().split("\n\n")
    lines = contents[0].split("\n")
    folds_str = contents[1].split("\n")
    folds = []
    regex = re.compile("([xy])=([0-9]+)")
    for fold_str in folds_str:
        match = regex.search(fold_str)
        if match:
            folds.append(Fold(match[1] == "x", int(match[2])))
        else:
            raise IOError(f"Invalid fold: {fold_str}")
    points = []
    x_list = []    # Probably not needed, but to remove it I need to look up some extra syntax
    y_list = []    # and that will take longer than just writing it this way.
    for line in lines:
        line = line.split(",")
        point = Point(int(line[0]), int(line[1]))
        x_list.append(point.x)
        y_list.append(point.y)
        points.append(point)
    return Paper(points, max(x_list) + 1, max(y_list) + 1, folds)


def main(input_filename: str):
    start_time = time.time()
    paper = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: {paper.fold(paper.folds[0])} points visible after first fold.")
    part2_start = time.time()
    print("Part 2:")
    paper.fold_all()
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day13.txt")
