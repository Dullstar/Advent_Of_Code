import time
import os
import enum
import collections


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Point({self.x},{self.y})"

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


sand_movement_priorities = [Point(0, 1), Point(-1, 1), Point(1, 1)]


class Tile(enum.IntEnum):
    Empty = 0
    Tile = 1
    Sand = 2


class Layout:
    def __init__(self, size_x, size_y, layout):
        self.size_x = size_x
        self.size_y = size_y
        self.layout = layout

    def __getitem__(self, pair):
        return self.layout[pair.y * self.size_x + pair.x]

    def __setitem__(self, pair, item):
        self.layout[pair.y * self.size_x + pair.x] = item

    def __repr__(self):
        x = 0
        output = f"Layout {self.size_x}x{self.size_y}\n"
        for tile in self.layout:
            match tile:
                case Tile.Tile:
                    output += "#"
                case Tile.Empty:
                    output += "."
                case Tile.Sand:
                    output += "o"
            x += 1
            if x == self.size_x:
                output += "\n"
                x = 0
        return output

    def drop_sand(self, spawner: Point):
        sand = spawner

        def try_move(sand_pos: Point):
            for direction in sand_movement_priorities:
                new_sand = sand_pos + direction
                if new_sand.x >= self.size_x or new_sand.x < 0 or new_sand.y >= self.size_y or self.size_y < 0:
                    return False, None  # Only the 2nd value matters from this return b/c None check is first.
                if self[new_sand] == Tile.Empty:
                    return True, new_sand
            return False, sand_pos

        while True:
            moved, sand = try_move(sand)
            if sand is None:
                return False
            if not moved:
                self[sand] = Tile.Sand
                return True

    def fill(self, spawner: Point):
        sand_pieces = 0
        while self.drop_sand(spawner):
            sand_pieces += 1
        return sand_pieces


# Used for Part 2. It has the problem of being quite slow, unfortunately. I browsed the megathread for some potential
# improvements and I'm noting down some I'd like to look into:
#     We don't actually need an infinite layout: We should be able to figure out the size of the worst case scenario
#     and simply preallocate the required amount of space!
#
#     We could fill the entire arena and then remove sand from spots where it can't reach. If we can determine those
#     locations faster than we can simulate each grain, it might just work.
class InfiniteLayout:
    def __init__(self, tiles, max_y):
        self.tiles = collections.defaultdict(lambda: Tile.Empty)
        for tile in tiles:
            self.tiles[tile] = Tile.Tile
        self.infinite_floor_y = max_y + 1

    def __getitem__(self, pt):
        return self.tiles[pt] if pt.y != self.infinite_floor_y else Tile.Tile

    def __repr__(self):
        output = ""
        min_x = min(self.tiles.keys(), key=lambda n: n.x).x
        max_x = max(self.tiles.keys(), key=lambda n: n.x).x
        for y in range(0, self.infinite_floor_y + 1):
            for x in range(min_x, max_x + 1):
                tile = self[Point(x, y)]
                match tile:
                    case Tile.Tile:
                        output += "#"
                    case Tile.Empty:
                        output += "."
                    case Tile.Sand:
                        output += "o"
            output += "\n"
        return output

    def drop_sand(self, spawner: Point):
        sand = spawner

        def try_move(sand_pos: Point):
            for direction in sand_movement_priorities:
                new_sand = sand_pos + direction
                if self[new_sand] == Tile.Empty:
                    return True, new_sand
            return False, sand_pos

        while True:
            moved, sand = try_move(sand)
            if sand is None:
                assert False
            if not moved:
                self.tiles[sand] = Tile.Sand
                if sand == spawner:
                    return False
                return True

    def fill(self, spawner: Point):
        sand_pieces = 0
        if self[spawner] == Tile.Tile:
            print("Honestly, I didn't think this case was possible, but 0 should be the right answer for it.")
            return 0
        while True:
            sand_pieces += 1
            if not self.drop_sand(spawner):
                break
        return sand_pieces


# Parse input returns got a bit messy after Part 2. It may be possible to clean up Part 1 to reuse the data structure.
# But I'm not sure I want to do it that way; it likely won't perform as well.
def parse_input(filename: str):
    tiles = set()

    def fill_tiles(first: Point, second: Point):
        assert (first.x == second.x) ^ (first.y == second.y)
        if first.x == second.x:
            ends = sorted([first.y, second.y])
            for y in range(ends[0], ends[1] + 1):
                tiles.add(Point(first.x, y))
        elif first.y == second.y:
            ends = sorted([first.x, second.x])
            for x in range(ends[0], ends[1] + 1):
                tiles.add(Point(x, first.y))

    with open(filename, "r") as file:
        for line in file:
            last_pair = None
            for pair in line.strip().split(" -> "):
                pair = [int(i) for i in pair.split(",")]
                pair = Point(pair[0], pair[1])
                if last_pair is not None:
                    fill_tiles(last_pair, pair)
                last_pair = pair
    max_x = max(tiles, key=lambda n: n.x).x + 1
    max_y = max(tiles, key=lambda n: n.y).y + 1
    min_x = min(tiles, key=lambda n: n.x).x
    size_x = max_x - min_x
    size_y = max_y
    layout = Layout(size_x, size_y, [Tile.Empty for _ in range(size_x * size_y)])
    for tile in tiles:
        layout[tile + Point(-min_x, 0)] = Tile.Tile
    sand_spawner = Point(500 - min_x, 0)
    infinite_spawner = Point(500, 0)
    infinite_layout = InfiniteLayout(tiles, max_y)
    return layout, sand_spawner, infinite_layout, infinite_spawner


def main(input_filename: str):
    start_time = time.time()
    cave, spawner, infinite_cave, infinite_spawner = parse_input(input_filename)
    part1_start = time.time()
    p1 = cave.fill(spawner)
    print(f"Part 1: {p1} sand units dispensed")
    part2_start = time.time()
    print("Part 2: ", end="")
    p2 = infinite_cave.fill(infinite_spawner)
    print(f"{p2} sand units dispensed")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day14.txt")


    run_main()
