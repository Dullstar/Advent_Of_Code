import time
import os
import queue


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Layout:
    def __init__(self, size_x, size_y, elevation):
        self.size_x = size_x
        self.size_y = size_y
        self.elevations = elevation
        self.costs_cache = None

    def __getitem__(self, pair):
        x, y = pair.x, pair.y
        return self.elevations[y * self.size_x + x]

    def get_coords_from_index(self, index: int):
        return Point((index % self.size_x), (index // self.size_x))

    def get_index_from_coords(self, coords: Point) -> int:  # Needed to get the indices for the costs list
        return coords.y * self.size_x + coords.x

    # This function isn't used, but the results make a somewhat interesting visualation so I think it's worth keeping
    def visualize_costs(self, costs):
        x = 0
        output = f"Costs {self.size_x}x{self.size_y}\n"
        for thing in costs:
            if thing is None:
                output += "--- "
            else:
                output += f"{thing:03} "
            x += 1
            if x == self.size_x:
                output += "\n"
                x = 0
        return output

    def find_path(self, start, end):
        if self.costs_cache is not None:
            return self.costs_cache[self.get_index_from_coords(start)]
        costs: list[None or int] = [None for _ in self.elevations]
        neighbors = [Point(0, 1), Point(1, 0), Point(-1, 0), Point(0, -1)]
        q = queue.SimpleQueue()
        q.put(end)
        costs[self.get_index_from_coords(end)] = 0
        while not q.empty():
            current = q.get()
            current_elevation = self[current]
            current_cost = costs[self.get_index_from_coords(current)]
            for neighbor in neighbors:
                test = neighbor + current
                if test.x < 0 or test.y < 0 or test.x >= self.size_x or test.y >= self.size_y:
                    continue
                test_elevation = self[test]
                if costs[self.get_index_from_coords(test)] is not None:
                    continue
                if current_elevation - test_elevation <= 1:
                    costs[self.get_index_from_coords(test)] = current_cost + 1
                    q.put(test)
        self.costs_cache = costs
        return costs[self.get_index_from_coords(start)]


def parse_input(filename: str):
    def char_to_int(character):
        return ord(character) - ord('a')

    elevations = []
    start, end = None, None
    with open(filename, "r") as file:
        for y, line in enumerate(file):
            line = line.strip()
            size_x = len(line)
            for x, char in enumerate(line):
                match char:
                    case "S":
                        start = Point(x, y)
                        elevations.append(char_to_int("a"))
                    case "E":
                        end = Point(x, y)
                        elevations.append(char_to_int("z"))
                    case other:
                        elevations.append(char_to_int(other))
    assert start is not None and end is not None
    return Layout(size_x, y + 1, elevations), start, end


def find_potential_starts(layout: Layout) -> list[Point]:
    # Grab the indices of each layout that has the desired starting elevation of 0 ("a" in the original input)
    filt = filter(lambda n: layout.elevations[n] == 0, range(len(layout.elevations)))
    # ...then convert all those indices to coordinates
    return [i for i in map(lambda m: layout.get_coords_from_index(m), filt)]


def find_best_start(layout: Layout, end: Point) -> int:
    starts = find_potential_starts(layout)
    # Some potential start locations can't reach the end (denoted by a cost of None), which is why we need to filter.
    return min(filter(lambda result: result is not None, map(lambda s: layout.find_path(s, end), starts)))


def main(input_filename: str):
    start_time = time.time()
    layout, start, end = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: Length of shortest past from start to end: {layout.find_path(start, end)}")
    part2_start = time.time()
    print(f"Part 2: Length of shortest past from any elevation 'a' to end: {find_best_start(layout, end)}")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day12.txt")

    run_main()
