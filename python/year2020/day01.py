import time
import os
import itertools as it


def parse_input(filename: str):
    numbers = []
    with open(filename, "r") as file:
        for line in file:
            numbers.append(int(line.strip()))

    return numbers


def find_two(numbers: list):
    for a, b in it.combinations(numbers, 2):
        if a + b == 2020:
            print(f"Part 1: Found {a} + {b} == 2020; product = {a * b}")
            return
    print("Failed to find two.")


def find_three(numbers: list):
    for a, b, c in it.combinations(numbers, 3):
        if a + b + c == 2020:
            print(f"Part 2: Found {a} + {b} + {c} == 2020; product = {a * b * c}")
            return
    print("Failed to find three.")


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    start_time = time.time()
    numbers = parse_input(input_filename)
    part1_start = time.time()
    find_two(numbers)
    part2_start = time.time()
    find_three(numbers)
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2020/day01.txt"
        main(filename)

    run_main()
