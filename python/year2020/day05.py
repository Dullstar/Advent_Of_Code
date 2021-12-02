import time
import os


def parse_input(filename: str):
    with open(filename, "r") as file:
        lines = []
        for line in file:
            lines.append(line.strip())
        return lines


def get_offset(letter: str, total_seats: int):
    offset = -1
    if letter == "F" or letter == "L":
        offset = 0
    elif letter == "B" or letter == "R":
        offset = total_seats // 2

    return offset


def interpret_pass(boarding_pass: str):
    current_num = 128
    offsets = []
    for i in range(7):
        offsets.append(get_offset(boarding_pass[i], current_num))
        current_num //= 2
    row = sum(offsets)
    offsets = []
    current_num = 8
    for i in range(7, 10):
        offsets.append(get_offset(boarding_pass[i], current_num))
        current_num //=2
    column = sum(offsets)
    return row, column


def main(input_filename: str):
    start_time = time.time()
    passes = parse_input(input_filename)
    part1_start = time.time()
    seats = []
    for boarding_pass in passes:
        row, column = interpret_pass(boarding_pass)
        seats.append(row * 8 + column)
    max_seat_id = max(seats)
    print(f"Part 1: The highest seat ID is {max_seat_id}")
    part2_start = time.time()

    min_seat_id = min(seats)
    # We actually do end up using this information in part 2, and it adds a little flavor to output it...
    # but we aren't actually asked for the result so it doesn't *need* to be outputted.
    print(f"Extra: The lowest seat ID is {min_seat_id}")

    ids_to_check = [x for x in range(min_seat_id + 1, max_seat_id)]  # don't need to check max and min
    for seat_id in ids_to_check:
        if seat_id not in seats:
            print(f"Part 2: The seat ID {seat_id} is not in the list of seats")
            break  # we've been told there should only be one, so we can stop when we find it
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2020/day05.txt")

    run_main()
