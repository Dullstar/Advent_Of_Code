import time
import os


class Layout:
    def __init__(self, size_x, size_y, trees):
        self.size_x = size_x
        self.size_y = size_y
        self.trees = trees

    def __getitem__(self, pair: tuple[int, int]):
        x, y = pair[0], pair[1]
        return self.trees[y * self.size_x + x]

    def get_coords_from_index(self, index: int):
        return (index // self.size_x), (index % self.size_x)

    def is_visible(self, x: int, y: int):
        if x == 0 or y == 0 or x == (self.size_x - 1) or y == (self.size_y - 1):
            return True

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # dx, dy pairs for check_dir

        def check_dir(dx, dy):
            cx, cy = x + dx, y + dy  # cx -> current_x
            start_height = self[x, y]
            while 0 <= cx < self.size_x and 0 <= cy < self.size_y:
                if self[cx, cy] >= start_height:
                    return False
                cx += dx
                cy += dy
            return True

        for direction in directions:
            if check_dir(direction[0], direction[1]):
                return True
        return False

    def count_visible(self):
        total = 0
        for i in range(len(self.trees)):
            x, y = self.get_coords_from_index(i)
            total += self.is_visible(x, y)
        return total

    def get_scenic_score(self, x: int, y: int):
        if x == 0 or y == 0 or x == (self.size_x - 1) or y == (self.size_y - 1):
            return 0  # We know these ones won't work.
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # dx, dy pairs for check_dir

        def check_dir(dx, dy):
            dir_score = 0
            cx, cy = x + dx, y + dy  # cx -> current_x
            start_height = self[x, y]
            while 0 <= cx < self.size_x and 0 <= cy < self.size_y:
                dir_score += 1
                if self[cx, cy] >= start_height:
                    return dir_score
                cx += dx
                cy += dy
            return dir_score

        score = 1
        for direction in directions:
            score *= check_dir(direction[0], direction[1])
        return score

    def get_best_scenic_score(self):
        score = 0
        for i in range(len(self.trees)):
            x, y = self.get_coords_from_index(i)
            score = max(score, self.get_scenic_score(x, y))
        return score


def parse_input(filename: str):
    trees = []
    size_x = 0
    size_y = 0
    with open(filename, "r") as file:
        for line in file:
            size_y += 1
            i = 0
            for char in line.strip():
                trees.append(int(char))
                i += 1
            size_x = i
    return Layout(size_x, size_y, trees)


def main(input_filename: str):
    start_time = time.time()
    trees = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: There are {trees.count_visible()} visible trees.")
    part2_start = time.time()
    print(f"Part 2: The best possible scenic score is {trees.get_best_scenic_score()}.")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day08.txt")

    run_main()

'''
Having a 2D layout printing function lying around could be pretty handy. Here's one that works with Layout.
Probably would need to rename tree though since it's not a literal plant tree...
    def __repr__(self):
        x = 0
        output = f"Layout {self.size_x}x{self.size_y}\n"
        for tree in self.trees:
            output += f"{tree}"
            x += 1
            if x == self.size_x:
                output += "\n"
                x = 0
        return output
'''