import time
import os


def parse_input(filename: str) -> list[int]:
    positions = []
    with open(filename, "r") as file:
        for i in file.read().strip().split(","):
            positions.append(int(i))
    return positions


def get_fuel_part1(positions: list[int], target_pos: int) -> int:
    usage = 0
    for position in positions:
        usage += abs(position - target_pos)
    return usage


def minimize_fuel_part1(positions: list[int]) -> int:
    usages = []
    for position in positions:
        usages.append(get_fuel_part1(positions, position))
    return min(usages)


def get_fuel_part2(positions: list[int], target_pos: int) -> int:
    usage = 0
    # print("----------------")
    for position in positions:
        move_size = abs(position - target_pos)
        # The fuel usage is the sum of the first move_size terms of the arithmetic series 1, 2, 3, 4 ...
        individual_usage = (move_size * ((1 + move_size) / 2))
        # print(f"Move from {position} to {target_pos}: {individual_usage}")
        usage += individual_usage

    return int(usage)


def minimize_fuel_part2(positions: list[int]) -> int:
    usages = []
    for position in range(min(positions), max(positions) + 1):
        usages.append(get_fuel_part2(positions, position))
    return min(usages)


def main(input_filename: str):
    start_time = time.time()
    positions = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: {minimize_fuel_part1(positions)} fuel is required.")
    part2_start = time.time()
    print(f"Part 2: {minimize_fuel_part2(positions)} fuel is required.")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day07.txt")
