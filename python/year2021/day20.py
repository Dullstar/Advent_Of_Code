import time
import os
import collections


Point = collections.namedtuple("Point", ["x", "y"])


class Layout:
    def __init__(self, points: dict[Point], enhancer: str):
        self.points = points
        self.enhancer = enhancer
        self.check = [
            Point(-1, -1), Point(0, -1), Point(1, -1),
            Point(-1, 0), Point(0, 0), Point(1, 0),
            Point(-1, 1), Point(0, 1), Point(1, 1)
        ]

    def expand(self, iteration: int):
        to_add = set()
        for point, value in self.points.items():
            for location in self.check:
                location = Point(point.x + location.x, point.y + location.y)
                if location not in self.points:
                    to_add.add(location)
        for location in to_add:
            self.points[location] = "0" if (iteration % 2 == 0) or (self.enhancer[0] == "0") else "1"

    def check_pixels(self, iteration: int):
        next_image = dict()
        for point, value in self.points.items():
            bin_string = ""
            for location in self.check:
                location = Point(point.x + location.x, point.y + location.y)
                if location in self.points:
                    bin_string += self.points[location]
                else:
                    # Edge handling. Assumes all middle values are filled in.
                    bin_string += "0" if (iteration % 2 == 0) or (self.enhancer[0] == "0") else "1"
            next_image[point] = self.enhancer[int(bin_string, 2)]
        self.points = next_image

    def enhance(self, iterations: int):
        for i in range(iterations):
            self.expand(i)
            self.check_pixels(i)
        total = 0
        for i in self.points.values():
            total += int(i)
        return total

    def __repr__(self):
        max_x = max(self.points.keys(), key=lambda n: n.x).x
        min_x = min(self.points.keys(), key=lambda n: n.x).x
        max_y = max(self.points.keys(), key=lambda n: n.y).y
        min_y = min(self.points.keys(), key=lambda n: n.y).y
        output = ""
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (p := Point(x, y)) in self.points:
                    output += "#" if self.points[p] == "1" else "."
                else:
                    # output += " " # commented for potential future restoration
                    assert False, \
                        "Parts of the code assume this shouldn't happen."
            output += "\n"
        return output


def parse_input(filename: str):
    with open(filename, "r") as file:
        contents = file.read().replace("#", "1").replace(".", "0").strip().split("\n\n")
    enhancer = contents[0]
    points = dict()
    x, y = 0, 0
    for char in contents[1]:
        if char == "\n":
            x = 0
            y += 1
            continue
        points[Point(x, y)] = char
        x += 1
    return Layout(points, enhancer)


def main(input_filename: str):
    start_time = time.time()
    layout = parse_input(input_filename)

    part1_start = time.time()
    print(f"Part 1: {layout.enhance(2)} lit pixels")

    part2_start = time.time()
    print(f"Part 2: {layout.enhance(48)} lit pixels")

    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day20.txt")
