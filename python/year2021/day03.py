import time
import os


def parse_input(filename: str) -> tuple[list[int], int]:
    with open(filename, "r") as file:
        nums = [int(line, 2) for line in file]
        file.seek(0)
        length = len(file.readline().strip())
    return nums, length


def get_most_common_bit(numbers: list[int], current_bit: int) -> int:
    total0 = 0
    total1 = 0
    for num in numbers:
        if current_bit & num:
            total1 += 1
        else:
            total0 += 1
    # It happens that this works out correctly even for the C02 scrubber, having to do with inverting the checks
    return current_bit if total1 >= total0 else 0


def find_gamma_and_epsilon(numbers: list[int], bits: int) -> tuple[int, int]:
    current_bit = 1
    gamma = 0
    for i in range(bits):
        gamma |= get_most_common_bit(numbers, current_bit)
        current_bit <<= 1
    mask = int("1" * bits, 2)  # there is probably a better way to generate this number
    epsilon = mask ^ gamma
    return gamma, epsilon


def find_rating(numbers: list[int], most_significant_bit_pos: int, *, is_o2: bool = False, is_co2: bool = False):
    # is_co2 exists mainly for clarity at the call site. It's used, but we could have just done (not is_o2)
    assert is_o2 != is_co2, "Exactly 1 of is_o2 and is_co2 must be True"
    bit = 1 << (most_significant_bit_pos - 1)
    want1 = bool(get_most_common_bit(numbers, bit))
    filtered = []
    for num in numbers:
        check = (want1 and (bit & num)) or (not want1) and (not (bit & num))
        if is_o2 and check:
            filtered.append(num)
        elif is_co2 and (not check):
            filtered.append(num)

    if bit != 1 and len(filtered) > 1:
        return find_rating(filtered, most_significant_bit_pos - 1, is_o2=is_o2, is_co2=is_co2)
    return filtered[0]


def main(input_filename: str):
    start_time = time.time()
    numbers, length = parse_input(input_filename)
    part1_start = time.time()
    gamma, epsilon = find_gamma_and_epsilon(numbers, length)
    print(f"Part 1: The product of gamma {gamma} and epsilon {epsilon} is {gamma * epsilon}")
    part2_start = time.time()
    o2 = find_rating(numbers, length, is_o2=True)
    co2 = find_rating(numbers, length, is_co2=True)
    print(f"Part 2: The product of o2 generator rating {o2} and co2 scrubber rating {co2} is {o2 * co2}")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day03.txt")
