import time
import os


def solve(order: list[int], iterations=1):
    indices = [i for i in range(len(order))]
    for _ in range(iterations):
        for i, number in enumerate(order):
            if number == 0:
                continue
            old_pos = indices[i]
            new_pos = (old_pos + number) % (len(order) - 1)
            for j in range(len(order)):
                if indices[j] > old_pos:
                    indices[j] = (indices[j] - 1) % len(order)
                if indices[j] >= new_pos:  # >= is because we need to also move the one that was ALREADY there.
                    indices[j] = (indices[j] + 1) % len(order)
            indices[i] = new_pos
    test = [None for _ in range(len(order))]
    for j in range(len(order)):
        test[indices[j]] = order[j]

    zero_index = test.index(0)
    return sum(map(lambda n: test[(zero_index + n) % len(test)], [1000, 2000, 3000]))


def parse_input(filename: str):
    with open(filename, "r") as file:
        return [int(line) for line in file]


def main(input_filename: str):
    start_time = time.time()
    numbers = parse_input(input_filename)
    part1_start = time.time()
    # numbers = parse_input("test_input.txt")
    print(f"Part 1: Grove coordinates sum: {solve(numbers)}")
    part2_start = time.time()
    numbers2 = [i * 811589153 for i in numbers]
    print(f"Part 2: Grove coordinates sum: {solve(numbers2, 10)}")
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
        main("../../inputs/2022/day20.txt")

    run_main()
