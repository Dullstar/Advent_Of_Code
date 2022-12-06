import time
import os


def parse_input(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def find_start(signal: str, marker_length):
    for i in range(len(signal) - marker_length + 1):
        chars = set(signal[i:i+marker_length])
        if len(chars) == marker_length:
            return i + marker_length
    raise Exception("Couldn't find one.")


def main(input_filename: str):
    start_time = time.time()
    signal = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: Packet detected after {find_start(signal, 4)} characters.")
    part2_start = time.time()
    print(f"Part 2: Message detected after {find_start(signal, 14)} characters.")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day06.txt")

    run_main()
