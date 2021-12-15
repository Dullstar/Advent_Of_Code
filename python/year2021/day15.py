import time
import os
import collections


Point = collections.namedtuple("Point", ["x", "y"])


class Map:
    def __init__(self, layout: list[int], size_x: int, size_y: int):
        self.layout = layout
        self.size_x = size_x
        self.size_y = size_y
        self.start: Point = Point(0, 0)
        self.end: Point = Point(size_x - 1, size_y - 1)

    def __getitem__(self, key: tuple[int, int]):
        # x, y = key  # contents of key
        return self.layout[key[0] + (key[1] * self.size_x)]

    def __setitem__(self, key: tuple[int, int], value):
        self.layout[key[0] + (key[1] * self.size_x)] = value

    def out_of_bounds(self, x: int, y: int):
        return (x < 0) or (y < 0) or (x >= self.size_x) or (y >= self.size_y)

    def find_path(self):
        found_path = False
        path_score = None
        board: list[int or None] = [None] * len(self.layout)
        board[-1] = 0  # The way this is organized, this should be equivalent to working out the index of self.end
        queue: collections.deque[Point] = collections.deque()
        queue.append(self.end)
        neighbors = [Point(0, -1), Point(-1, 0), Point(0, 1), Point(1, 0)]
        while len(queue) > 0:
            current = queue.popleft()
            current_index = current.y * self.size_x + current.x
            for neighbor in neighbors:
                neighbor = Point(neighbor.x + current.x, neighbor.y + current.y)
                neighbor_index = neighbor.y * self.size_x + neighbor.x
                if not self.out_of_bounds(neighbor.x, neighbor.y):
                    new_value = board[current_index] + self.layout[current_index]
                    if (board[neighbor_index] is None) or (board[neighbor_index] > new_value):
                        board[neighbor_index] = new_value
                        queue.append(neighbor)

        '''n = 0
        string = ""
        for item in board:
            string += (f"{item:03} " if item is not None else "--- ")
            n += 1
            if n == self.size_x:
                string += "\n"
                n = 0
        return string'''
        return board[0]

    def grow(self, grow_x, grow_y):
        # Maybe we could do this with a list comprehension, but I'm not even going to try, as I don't think the
        # resulting statement would be readable at all.
        new_size_x = self.size_x * grow_x
        new_size_y = self.size_y * grow_y
        new_layout = [0] * new_size_x * new_size_y
        for y in range(new_size_y):
            for x in range(new_size_x):
                check_x = x % self.size_x
                check_y = y % self.size_y
                add_x = x // self.size_x
                add_y = y // self.size_y
                # Uses some math to find the correct number.
                # The -1 / +1 exists to take the 1-9, remap it to 0-8 so we can use %, then return it to 1-9.
                new_layout[y * new_size_x + x] = (self[check_x, check_y] - 1 + add_x + add_y) % 9 + 1
        self.layout = new_layout
        self.size_x = new_size_x
        self.size_y = new_size_y
        self.end = Point(self.size_x - 1, self.size_y - 1)

    def __str__(self):
        n = 0
        string = ""
        for item in self.layout:
            string += str(item)
            n += 1
            if n == self.size_x:
                string += "\n"
                n = 0
        return string


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
    risks = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: {risks.find_path()}")
    part2_start = time.time()
    risks.grow(5, 5)
    part2_expansion = time.time()
    print("Part 2 (this may take a while): ", end="")
    print(risks.find_path())
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms; ", end="")
    print(f"Expansion: {(part2_expansion - part2_start) * 1000:.2f} ms; Path: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day15.txt")
