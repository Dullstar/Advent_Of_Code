import time
import os


def parse_input(filename: str) -> list[int]:
    with open(filename, "r") as file:
        nums = [int(line) for line in file]
    return nums


def get_depth_increases(readings: list[int]) -> int:
    total = 0
    for i in range(1, len(readings)):
        if readings[i] > readings[i - 1]:
            total += 1
    return total


def sliding_window_increases(readings: list[int]) -> int:
    total = 0
    sums = []
    for i in range(len(readings) - 2):
        sums.append(readings[i] + readings[i + 1] + readings[i + 2])
    return get_depth_increases(sums)


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    start_time = time.time()
    readings = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: {get_depth_increases(readings)} depth increases")
    part2_start = time.time()
    print(f"Part 2: {sliding_window_increases(readings)} depth increases (sliding window)")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")
    return -1


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2021/day01.txt"
        main(filename)

    run_main()
