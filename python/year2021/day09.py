import time
import os
import collections


Point = collections.namedtuple("Point", ["x", "y"])
LowPoint = collections.namedtuple("LowPoint", ["point", "value"])


class Map:
    def __init__(self, layout: list[int], size_x: int, size_y: int):
        self.layout = layout
        self.size_x = size_x
        self.size_y = size_y
        self._low_points = None

    def __getitem__(self, key: tuple[int, int]):
        # x, y = key  # contents of key
        return self.layout[key[0] + (key[1] * self.size_x)]

    def find_low_points(self):
        if self._low_points is not None:
            return self._low_points
        low_points = []
        adjacent = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for y in range(self.size_y):
            for x in range(self.size_x):
                is_lowest = True
                for ax, ay in adjacent:
                    if (x + ax >= 0) and (x + ax < self.size_x) and (y + ay >= 0) and (y + ay < self.size_y) \
                            and (self[x + ax, y + ay] <= self[x, y]):
                        is_lowest = False
                        break
                if is_lowest:
                    low_points.append(LowPoint(Point(x, y), self[x, y]))
        self._low_points = low_points
        return low_points

    def get_low_point_risk_levels(self):
        return [i.value + 1 for i in self.find_low_points()]

    def find_basins_product(self):
        basin_map = [-1] * len(self.layout)

        def push_neighbors(x: int, y: int, value: int):
            basin_map[x + (y * self.size_x)] = value
            adjacent = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for ax, ay in adjacent:
                if (x + ax < 0) or (x + ax >= self.size_x) or (y + ay < 0) or (y + ay >= self.size_y)\
                        or (basin_map[x + ax + ((y + ay) * self.size_x)] != -1) or (self[x + ax, y + ay] == 9):
                    continue
                push_neighbors(x + ax, y + ay, value)

        # we just use i here as a unique id; enumerate just happens to be a convenient way to generate them - we
        # really don't care what it is as long as no two low points get assinged to the same one.
        for i, low_point in enumerate(self.find_low_points()):
            push_neighbors(low_point.point.x, low_point.point.y, i)

        basin_sizes = collections.Counter()
        for point in basin_map:
            if point != -1:
                basin_sizes[point] += 1
        temp = basin_sizes.most_common(3)
        return temp[0][1] * temp[1][1] * temp[2][1]


def parse_input(filename: str) -> Map:
    with open(filename, "r") as file:
        raw_contents = file.read()
        contents = [int(i) for i in raw_contents.replace("\n", "")]
        raw_contents = raw_contents.split()
        size_x = len(raw_contents[0])
        size_y = len(raw_contents)
        return Map(contents, size_x, size_y)


def main(input_filename: str):
    start_time = time.time()
    vent_map = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: Sum of risk levels: {sum(vent_map.get_low_point_risk_levels())}")
    part2_start = time.time()
    print(f"Part 2: Product of 3 largest basin sizes: {vent_map.find_basins_product()}")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day09.txt")
