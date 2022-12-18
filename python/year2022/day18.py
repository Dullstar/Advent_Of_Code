import time
import os
import functools
from collections import namedtuple
import queue

Point3D = namedtuple("Point3D", "x y z")
Boundaries = namedtuple("Boundaries", "max min")


def get_boundaries(cubes: set[Point3D]):
    max_x = max(cubes, key=lambda n: n.x).x
    max_y = max(cubes, key=lambda n: n.y).y
    max_z = max(cubes, key=lambda n: n.z).z
    min_x = min(cubes, key=lambda n: n.x).x
    min_y = min(cubes, key=lambda n: n.y).y
    min_z = min(cubes, key=lambda n: n.z).z
    return Boundaries(Point3D(max_x, max_y, max_z), Point3D(min_x, min_y, min_z))


def get_cube_neighbor_count(cube: Point3D, cubes: set[Point3D], surrounded=None):
    if surrounded is None:
        surrounded = set()
    relative = [Point3D(-1, 0, 0), Point3D(1, 0, 0),
                Point3D(0, -1, 0), Point3D(0, 1, 0),
                Point3D(0, 0, -1), Point3D(0, 0, 1)]
    neighbors = map(lambda n: Point3D(n.x + cube.x, n.y + cube.y, n.z + cube.z), relative)
    return functools.reduce(lambda count, n: count + (n in cubes or n in surrounded), neighbors, 0)


def calculate_cube_surface_area(cube: Point3D, cubes: set[Point3D], surrounded=None):
    return 6 - get_cube_neighbor_count(cube, cubes, surrounded)


def get_empty_neighbors(cube: Point3D, cubes: set[Point3D]):
    relative = [Point3D(-1, 0, 0), Point3D(1, 0, 0),
                Point3D(0, -1, 0), Point3D(0, 1, 0),
                Point3D(0, 0, -1), Point3D(0, 0, 1)]
    neighbors = map(lambda n: Point3D(n.x + cube.x, n.y + cube.y, n.z + cube.z), relative)
    return [x for x in filter(lambda n: n not in cubes, neighbors)]


surrounded_cache: dict[Point3D: bool] = dict()


def is_surrounded(empty_cube, cubes, boundaries):
    if empty_cube in surrounded_cache:
        return surrounded_cache[empty_cube]
    found = set()
    neighbors = [Point3D(-1, 0, 0), Point3D(1, 0, 0),
                 Point3D(0, -1, 0), Point3D(0, 1, 0),
                 Point3D(0, 0, -1), Point3D(0, 0, 1)]
    q = queue.SimpleQueue()
    q.put(empty_cube)
    found.add(empty_cube)

    # Can return this function to return and cache the found stuff in one go!
    def reusable_return_bit(output: bool):
        for visited_cube in found:
            surrounded_cache[visited_cube] = output
        return output

    while not q.empty():
        current = q.get()
        for n in neighbors:
            test = Point3D(n.x + current.x, n.y + current.y, n.z + current.z)
            if test in surrounded_cache:
                return reusable_return_bit(surrounded_cache[test])  # If our neighbor is/isn't surrounded, we are too!
            if test.x < boundaries.min.x or test.y < boundaries.min.y or test.z < boundaries.min.z \
                    or test.x > boundaries.max.x or test.y > boundaries.max.y or test.z > boundaries.max.z:
                return reusable_return_bit(False)  # We hit a boundary, so this must be outside
            if test in found or test in cubes:
                continue
            q.put(test)  # Only hapepns if ALL conditionals are failed.
            found.add(test)
    # If we run out of stuff without reaching the droplet's bounding box, then there isn't a path there,
    # thus this particular cube is surrounded, i.e. it is on the interior of the droplet
    return reusable_return_bit(True)


def parse_input(filename: str) -> set[Point3D]:
    pts = set()
    with open(filename, "r") as file:
        for line in file:
            pt = line.strip().split(",")
            pts.add(Point3D(int(pt[0]), int(pt[1]), int(pt[2])))
    return pts


def main(input_filename: str):
    start_time = time.time()
    cubes = parse_input(input_filename)
    part1_start = time.time()
    pt1 = sum(map(lambda n: calculate_cube_surface_area(n, cubes), cubes))
    print(f"Part 1: Total surface area: {pt1}")
    part2_start = time.time()
    empty_cubes = functools.reduce(lambda _set, n: _set.union(get_empty_neighbors(n, cubes)), cubes, set())
    boundaries = get_boundaries(cubes)
    surrounded_cubes = set(filter(lambda cube: is_surrounded(cube, cubes, boundaries), empty_cubes))
    pt2 = sum(map(lambda n: calculate_cube_surface_area(n, cubes, surrounded_cubes), cubes))
    end_time = time.time()
    print(f"Part 2: Total surface area: {pt2}")
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day18.txt")

    run_main()
