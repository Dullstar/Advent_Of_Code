import time
import os


class Slope:
    def __init__(self, dx: int, dy: int):
        self.dx: int = dx
        self.dy: int = dy


class Map:
    # This constructor appears to be the slowest part.
    # But it's still fast enough that it's probably not worth the time it would take to optimize.
    def __init__(self, filename: str):
        self.map: list[str] = []
        with open(filename, "r") as file:
            for line in file:
                self.map.append(line.strip())
        self.len_x: int = len(self.map[0])
        self.len_y: int = len(self.map)

    def get_pos(self, x: int, y: int) -> None or str:
        if y >= self.len_y:  # Signifies we've reached the bottom
            return None
        else:
            return self.map[y][x % self.len_x]

    def count_trees(self, slope: Slope) -> int:
        trees = 0
        x = 0
        y = 0
        while True:
            current_pos = self.get_pos(x, y)
            if current_pos is None:
                break
            elif current_pos == "#":
                trees += 1
            x += slope.dx
            y += slope.dy
        return trees


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    start_time = time.time()
    tree_map = Map(input_filename)
    part1_start = time.time()
    product = tree_map.count_trees(Slope(3, 1))  # var name will make more sense in pt2; it pt1 it's just a temp
    print(f"Part 1 (dx, dy = 3, 1): Encountered {product} trees")
    part2_start = time.time()
    slopes = [Slope(1, 1), Slope(5, 1), Slope(7, 1), Slope(1, 2)]
    for slope in slopes:
        temp = tree_map.count_trees(slope)
        print(f"dx, dy = {slope.dx}, {slope.dy}: Encountered {temp} trees")
        product *= temp
    print("Part 2: Product of tree counts:", product)
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")
    return


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2020/day03.txt"
        main(filename)

    run_main()
