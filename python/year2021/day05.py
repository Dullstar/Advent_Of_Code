import time
import os
import collections

Point = collections.namedtuple("Point", ["x", "y"])
Line = collections.namedtuple("Line", ["start", "end"])


class Board:
    def __init__(self):
        self.layout = dict()
        self.layout_pt1 = dict()

    def place_line(self, line: Line):
        def gen_coordinates(start, end) -> (list[int], bool):
            flat = False
            if start == end:
                coords = [start]
                flat = True
            elif start < end:
                coords = [i for i in range(start, end + 1)]
            else:
                coords = [i for i in range(start, end - 1, -1)]
            return coords, flat

        x_coords, flat_x = gen_coordinates(line.start.x, line.end.x)
        y_coords, flat_y = gen_coordinates(line.start.y, line.end.y)

        assert(flat_x or flat_y or (len(y_coords) == len(x_coords)))

        for i in range(max(len(x_coords), len(y_coords))):
            # Either both x_coords and y_coords have the same length, or one of them has length 1
            # Using [i % len] makes it so we just keep reading [0] if the line was horizontal/vertical,
            # and is otherwise equivalent to [i]
            x = x_coords[i % len(x_coords)]
            y = y_coords[i % len(y_coords)]
            self.place_point((x, y), self.layout)
            if flat_x or flat_y:
                self.place_point((x, y), self.layout_pt1)

    @staticmethod
    def place_point(point: Point or tuple[int, int], layout: dict):
        if (point[0], point[1]) in layout:
            layout[point[0], point[1]] += 1
        else:
            layout[point[0], point[1]] = 1

    @staticmethod
    def count(layout: dict):
        total = 0
        for value in layout.values():
            if value >= 2:
                total += 1
        return total

    @staticmethod
    # Generates a diagram like the one shown in the example.
    # That said, the real input is very large and so this wouldn't be helpful in pretty much any console I've ever used
    # But it is helpful for making sure the test input is as expected.
    def debug(size_x, size_y, layout: dict):
        for y in range(size_y):
            for x in range(size_x):
                print(layout[x, y], end="") if (x, y) in layout else print(".", end="")
            print()


def parse_input(filename: str) -> list[Line]:
    lines = []
    with open(filename, "r") as file:
        for line in file:
            line = line.split(" -> ")
            start = [int(i) for i in line[0].split(",")]
            end = [int(i) for i in line[1].split(",")]
            lines.append(Line(Point(start[0], start[1]), Point(end[0], end[1])))
    return lines


def main(input_filename: str):
    start_time = time.time()
    lines = parse_input(input_filename)
    board = Board()
    part1_start = time.time()
    for line in lines:
        board.place_line(line)
    print(f"Part 1: {board.count(board.layout_pt1)} intersections")
    print(f"Part 2: {board.count(board.layout)} intersections")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1 + Part 2: {(end_time - part1_start) * 1000:.2f} ms (evaluation is combined today)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day05.txt")
