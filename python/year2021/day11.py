import time
import os
import collections


Point = collections.namedtuple("Point", ["x", "y"])


class Map:
    # Potential design improvement: maybe this should keep track of the current step
    def __init__(self, layout: list[int], size_x: int, size_y: int):
        self.layout = layout
        self.size_x = size_x
        self.size_y = size_y
        self.simultaneous_flash_step = None

    def __getitem__(self, key: tuple[int, int]):
        # x, y = key  # contents of key
        return self.layout[key[0] + (key[1] * self.size_x)]

    def __setitem__(self, key: tuple[int, int], value):
        self.layout[key[0] + (key[1] * self.size_x)] = value

    def process_step(self, step: int):
        flash_total = 0
        for y in range(self.size_y):
            for x in range(self.size_x):
                self[x, y] += 1
                if self[x, y] >= 10:
                    flash_total += self.flash(x, y)
        # Clean up
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self[x, y] >= 10:
                    self[x, y] = 0
        if sum(self.layout) == 0:
            self.simultaneous_flash_step = step
        return flash_total

    def flash(self, x, y):
        total = 0
        if self[x, y] == 10:
            total += 1
            adjacent = [(0, -1), (-1, 0), (0, 1), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for ax, ay in adjacent:
                ax += x
                ay += y
                if (ax >= 0) and (ax < self.size_x) and (ay >= 0) and (ay < self.size_y):
                    if self[ax, ay] < 10:
                        self[ax, ay] += 1
                        if self[ax, ay] == 10:
                            total += self.flash(ax, ay)
        return total

    def run_steps(self, minimum_number_to_run: int):
        # A bit hacky to shoehorn in Part 2.
        # Might refactor later, idk.
        # Returns the number of flashes that have occurred at the minimum number to run.
        total = 0
        step = 1
        while self.simultaneous_flash_step is None or step <= minimum_number_to_run:
            add = self.process_step(step)
            if step <= minimum_number_to_run:
                total += add
            step += 1
        return total

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
    print("Octopi is the superior plural because I think it's funny and that's what matters.")
    start_time = time.time()
    octopus_map = parse_input(input_filename)
    part1_start = time.time()
    print(f"At step 100, octopi have flashed {octopus_map.run_steps(100)} times")
    print(f"All octopi flash simultaneously at step {octopus_map.simultaneous_flash_step}")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1 + Part 2: {(end_time - part1_start) * 1000:.2f} ms (evaluation is combined today)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day11.txt")
