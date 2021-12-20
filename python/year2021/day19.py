import time
import os
import collections
import itertools


Point = collections.namedtuple("Point", ["x", "y", "z"])


class Beacon:
    def __init__(self, x: int, y: int, z: int):
        self.x: int = x
        self.y: int = y
        self.z: int = z
        self.orig = Point(x, y, z)
        self.current_rotation = Point(x, y, z)

    def rotate(self, rotation_id: int):
        global rotations
        rotation = rotations[rotation_id]
        rotation = (rotation.x, rotation.y, rotation.z)
        new = [self.orig[abs(rotation[0]) - 1], self.orig[abs(rotation[1]) - 1], self.orig[abs(rotation[2]) - 1]]
        for i in range(3):
            if rotation[i] < 0:
                new[i] *= -1
        self.x = new[0]
        self.y = new[1]
        self.z = new[2]
        self.current_rotation = Point(self.x, self.y, self.z)

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.z} -- orig: {self.orig}; rot: {self.current_rotation}"


# Lookup table for rotations. parse_input will assemble this.
rotations: list[Point] = []


class Scanner:
    def __init__(self, beacons: list[Beacon]):
        self.beacons: list[Beacon] = beacons
        self.current_pos = Point(0, 0, 0)

    def __repr__(self):
        output = ""
        for beacon in self.beacons:
            output += f"{beacon.x}, {beacon.y}, {beacon.z}\n"
        return output

    def rotate(self, rotation_id: int):
        for beacon in self.beacons:
            beacon.rotate(rotation_id)

    def set_pos(self, x: int, y: int, z: int):
        self.current_pos = Point(x, y, z)
        for beacon in self.beacons:
            beacon.x = beacon.current_rotation.x + x
            beacon.y = beacon.current_rotation.y + y
            beacon.z = beacon.current_rotation.z + z


class Layout:
    def __init__(self):
        self.beacons: set[Point] = set()
        self.scanners: list[Point] = []

    def add_scanner(self, scanner: Scanner, x: int, y: int, z: int):
        self.scanners.append(Point(x, y, z))
        for beacon in scanner.beacons:
            # Assumes the beacon's positions were already adjusted prior to adding the scanner.
            self.beacons.add(Point(beacon.x, beacon.y, beacon.z))

    def assemble(self, scanners: list[Scanner]):
        scanner_total = len(scanners)
        self.add_scanner(scanners.pop(0), 0, 0, 0)
        print(f"Filled in scanner {len(self.scanners)} of {scanner_total}")
        while len(scanners) > 0:
            next_scanner = False
            for i in range(len(scanners)):
                for rotation_id in range(len(rotations)):
                    scanners[i].rotate(rotation_id)
                    for j in range(len(scanners[i].beacons)):
                        for point in self.beacons:
                            scanners[i].set_pos(point.x - scanners[i].beacons[j].current_rotation.x,
                                                point.y - scanners[i].beacons[j].current_rotation.y,
                                                point.z - scanners[i].beacons[j].current_rotation.z)
                            give_up_threshold = len(scanners[i].beacons) - 11
                            failures = 0
                            successes = 0
                            for beacon in scanners[i].beacons:
                                works = Point(beacon.x, beacon.y, beacon.z) in self.beacons
                                successes += works
                                failures += not works
                                if failures > give_up_threshold or successes == 12:
                                    break
                            if successes == 12:
                                to_add = scanners.pop(i)
                                self.add_scanner(to_add,
                                                 to_add.current_pos.x,
                                                 to_add.current_pos.y,
                                                 to_add.current_pos.z)
                                next_scanner = True
                                break
                        if next_scanner:
                            break
                    if next_scanner:
                        break
                if next_scanner:
                    break
            if not next_scanner:
                raise Exception(f"Didn't find anything!")
            else:
                print(f"Filled in scanner {len(self.scanners)} of {scanner_total}")

    def save(self, filename, parse_duration, part1_duration):
        with open(filename, "w") as file:
            file.write(f"parse_time:{parse_duration}\n")
            file.write(f"part1_time:{part1_duration}\n")
            file.write("\n")
            file.write("beacons\n")
            for beacon in sorted(self.beacons):
                file.write(f"{beacon.x},{beacon.y},{beacon.z}\n")
            file.write("\n")
            file.write("scanners\n")
            for scanner in sorted(self.scanners):
                file.write(f"{scanner.x},{scanner.y},{scanner.z}\n")

    def load(self, filename):
        with open(filename, "r") as file:
            contents = file.read()
        contents = contents.split("\n\n")
        times = contents[0].strip().split("\n")
        parse_duration = float(times[0].split(":")[1])
        part1_duration = float(times[1].split(":")[1])
        for beacon in contents[1].strip().split("\n")[1:]:
            beacon = beacon.split(",")
            self.beacons.add(Point(int(beacon[0]), int(beacon[1]), int(beacon[2])))
        for scanner in contents[2].strip().split("\n")[1:]:
            scanner = scanner.split(",")
            self.scanners.append(Point(int(scanner[0]), int(scanner[1]), int(scanner[2])))
        return parse_duration, part1_duration, len(self.beacons)

    def find_biggest_manhattan_distance(self):
        distances = []
        for scan1, scan2 in itertools.combinations(self.scanners, 2):
            distances.append(abs(scan1.x - scan2.x) + abs(scan1.y - scan2.y) + abs(scan1.z - scan2.z))
        return max(distances)


def parse_input(filename: str):
    global rotations
    with open(filename, "r") as file:
        contents = file.read()
        contents = contents.split("\n\n")
    scanners = []
    for scanner in contents:
        beacons = []
        for beacon in scanner.strip().split("\n")[1:]:
            beacon = beacon.split(",")
            beacons.append(Beacon(int(beacon[0]), int(beacon[1]), int(beacon[2])))
        scanners.append(Scanner(beacons))
    prefix = ""
    if not os.path.exists("day19_rotations.txt"):
        prefix = "year2021/"
    with open(f"{prefix}day19_rotations.txt", "r") as file:
        for line in file:
            line = line.split(",")
            rotations.append(Point(int(line[0]), int(line[1]), int(line[2])))
    return scanners


def main(input_filename: str):
    # This seems pointless, but it's here because when using the test input, we just ignore the input_filename argument,
    # due to how the launcher currently supplies this argument as well as when the script is run independently.
    # Perhaps a proper setup for calling test inputs could be helpful, but it's not a priority at this time.
    filename = input_filename
    prefix = ""
    if not os.path.exists("day19_rotations.txt"):
        prefix = "year2021/"
    result_filename = f"{prefix}{os.path.basename(filename).split('.')[0]}_part1_layout_result.txt"
    load_result = False
    if os.path.exists(result_filename):
        while True:
            print("A previous run of Part 1 is saved. Would you like to load it? [y/n]")
            load_result = input().lower()
            if load_result == "y":
                load_result = True
                break
            elif load_result == "n":
                load_result = False
                break
            print("Invalid response:", load_result)
    if load_result:
        layout = Layout()
        load_start = time.time()
        parse_time, part1_time, beacon_count = layout.load(result_filename)
        load_end = time.time()
        io_time = load_end - load_start
    else:
        start_time = time.time()
        scanners = parse_input(filename)

        part1_start = time.time()
        layout = Layout()
        layout.assemble(scanners)
        beacon_count = len(layout.beacons)

        save_start = time.time()
        parse_time = part1_start - start_time
        part1_time = save_start - part1_start
        layout.save(result_filename, parse_time, part1_time)
        save_end = time.time()
        io_time = save_end - save_start
    print(f"Part 1: There are {beacon_count} beacons")
    part2_start = time.time()
    print(f"Part 2: The largest Manhattan distance between scanners is {layout.find_biggest_manhattan_distance()}")
    end_time = time.time()
    part2_time = end_time - part2_start

    print("Elapsed Time:")
    if load_result:
        print("    Parsing and Part 1 run times are based on the original saved run.")
        print(f"    Loading Part 1 result: {io_time * 1000:.2f} ms")
    print(f"    Parsing: {parse_time * 1000:.2f} ms")
    print(f"    Part 1: {part1_time * 1000:.2f} ms ", end="")
    print(f"({part1_time / 60:.2f} minutes)")
    if not load_result:
        print(f"    Saving Part 1 result: {io_time * 1000:.2f} ms")
    print(f"    Part 2: {part2_time * 1000:.2f} ms")
    print(f"    Total: {(parse_time + part1_time + part2_time + io_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day19.txt")
