import time
import os
import collections
import re
import functools

X_AXIS = 0
Y_AXIS = 1


# To save a little time it's not enforced by the class itself, but it does assume that first and second are in order
# from least to greatest, and that when checking for overlap, other.first > self.first
class Range:  # Not to be confused with the Python built-in
    def __init__(self, first: int, second: int):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"Range {self.first} to {self.second}"

    def overlaps(self, other):
        return other.first <= self.second

    def merge(self, other):
        return Range(self.first, max(self.second, other.second))

    def total_len(self):
        return self.second - self.first


class Point(collections.namedtuple("Point", "x y")):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def get_manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Sensor:
    def __init__(self, location: Point, beacon: Point):
        self.location = location
        self.beacon = beacon
        self.distance = location.get_manhattan_distance(beacon)

    def __repr__(self):
        return f"Sensor: {self.location}, beacon {self.beacon}\n    Distance: {self.distance}"

    '''def add_ranges(self, axis, ranges):
        center = self.location.x if axis == X_AXIS else self.location.y
        other = self.location.x if axis == Y_AXIS else self.location.y
        if center not in ranges:
            ranges[center] = []
        ranges[center].append(Range(other - self.distance, other + self.distance))
        for x in range(1, self.distance + 1):
            dist = self.distance - x
            if center + x not in ranges:
                ranges[center + x] = []
            ranges[center + x].append(Range(other - dist, other + dist))
            if center - x not in ranges:
                ranges[center - x] = []
            ranges[center - x].append(Range(other - dist, other + dist))'''

    def get_range(self, axis, target, ranges: list[Range]):
        center = self.location.x if axis == X_AXIS else self.location.y
        other = self.location.x if axis == Y_AXIS else self.location.y

        remain = self.distance - abs(center - target)
        if remain >= 0:
            ranges.append(Range(other - remain, other + remain))

    def get_surrounding_points(self) -> Point:
        distance = self.distance + 1  # It HAS to be next to a beacon
        yield Point(self.location.x, self.location.y + distance)
        yield Point(self.location.x, self.location.y - distance)
        for dx in range(1, distance):
            yield Point(self.location.x + dx, self.location.y + distance - dx)
            yield Point(self.location.x - dx, self.location.y + distance - dx)
            yield Point(self.location.x + dx, self.location.y - distance + dx)
            yield Point(self.location.x - dx, self.location.y - distance + dx)
        yield Point(self.location.x + distance, self.location.y)
        yield Point(self.location.x - distance, self.location.y)


def solve_part_1(sensors, target):
    ranges = []
    for sensor in sensors:
        sensor.get_range(Y_AXIS, target, ranges)
    ranges.sort(key=lambda n: n.first)
    new_ranges = []
    did_merge = True
    while did_merge:
        did_merge = False
        for i in range(len(ranges) - 1):
            if ranges[i].overlaps(ranges[i + 1]):
                merge = ranges[i].merge(ranges[i + 1])
                new_ranges.append(merge)
                cursed_bug_stopper = len(ranges)
                for j in range(i + 2, cursed_bug_stopper):
                    new_ranges.append(ranges[j])
                did_merge = True
                ranges = new_ranges
                new_ranges = []
                break
            new_ranges.append(ranges[i])
    return sum(map(lambda n: n.total_len(), ranges))


def solve_part_2(sensors: list[Sensor], limit):
    @functools.lru_cache()  # it was worth a shot
    def check_pt(p: Point):
        if p.x < 0 or p.y < 0 or p.x > limit or p.y > limit:
            return False
        for inner_sensor in sensors:
            dist = pt.get_manhattan_distance(inner_sensor.location)
            if dist <= inner_sensor.distance:
                return False
        return True

    for sensor in sensors:
        for pt in sensor.get_surrounding_points():
            if check_pt(pt):
                return pt


def parse_input(filename: str):
    regex = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    sensors = []
    with open(filename, "r") as file:
        for line in file:
            match = regex.match(line)
            assert match is not None
            sensors.append(Sensor(
                Point(int(match[1]), int(match[2])),
                Point(int(match[3]), int(match[4]))
            ))
    return sensors


def main(input_filename: str):
    start_time = time.time()
    sensors = parse_input(input_filename)
    target = 2000000  # These values are here so they can be modified easily if running test input
    limit = 4000000
    part1_start = time.time()
    pt1 = solve_part_1(sensors, target)
    print(f"Part 1: y = {target} has {pt1} occupied spaces.")
    part2_start = time.time()
    pt2 = solve_part_2(sensors, limit)
    print(f"Part 2: The distress beacon's tuning frequency is {pt2.x} * 4000000 + {pt2.y} = {pt2.x * 4000000 + pt2.y}")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day15.txt")

    run_main()
