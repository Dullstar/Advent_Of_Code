import time
import os


def parse_input(filename):
    output = []
    with open(filename, "r") as file:
        for line in file:
            output.append(int(line.strip()))
    return output


# Assumes the adapters list is sorted.
def get_deltas(adapters: list, output: bool = True):
    prev_voltage = 0
    delta_dict = {}
    for adapter in adapters:
        delta = adapter - prev_voltage
        if delta not in delta_dict:
            delta_dict[delta] = 1
        else:
            delta_dict[delta] += 1
        prev_voltage = adapter

    if output:
        # The following may not be safe for arbitrary inputs, since we've assumed some stuff exists

        # Accounts for a provision in the problem regarding the final adapter in the chain
        delta_dict[3] += 1
        print("Distribution:")
        for key in sorted(delta_dict.keys()):
            print(f"Delta = {key} occurs {delta_dict[key]} times.")
        print(f"Part 1: Product of 1 and 3 differences: {delta_dict[1] * delta_dict[3]}")
    return delta_dict


def find_next(start: int, adapters_ints: list, known_results=None):
    # Recursion termination conditions: hit the end, or run out of further leads
    found = 0
    if known_results is None:
        known_results = {}
    if start == adapters_ints[-1]:
        return 1
    for i in range(1, 4):
        if start + i in adapters_ints:
            if start + i not in known_results:
                known_results[start + i] = find_next(start + i, adapters_ints, known_results)
            found += known_results[start + i]
    return found


def find_valid_connections(adapters: list):
    found = find_next(0, adapters)
    print(f"Part 2: Found {found} possibilities")
    return


def main(input_filename: str):
    start_time = time.time()
    adapters = parse_input(input_filename)
    part1_start = time.time()
    adapters.sort()
    get_deltas(adapters)
    part2_start = time.time()
    find_valid_connections(adapters)
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2020/day10.txt")
