import time
import os
class XMAS:
    def __init__(self, numbers: list, preamble_size: int):
        self.numbers = numbers
        self.preamble_size = preamble_size

        # could just use preamble_size, but start_index makes it easier to communicate intent later
        # or to future-proof if there's a similar problem where we don't want to start right after the preamble
        self.start_index = self.preamble_size

    def validate(self, index):
        for i in range(index - self.preamble_size, index):
            for j in range(index - self.preamble_size, index):
                if i != j:  # don't want to add this to itself unless the value is duplicated
                    if self.numbers[i] + self.numbers[j] == self.numbers[index]:
                        return True
        return False

    def get_weakness_from_cont_range(self, start_index: int, end_index: int):
        cont_range_list = [self.numbers[i] for i in range(start_index, end_index + 1)]
        smallest = min(cont_range_list)
        largest = max(cont_range_list)
        print(f"Found the range! It covers indices {start_index} to {end_index}")
        print(f"with the numbers min = {smallest} and max = {largest}.")
        return smallest + largest

    def cont_range(self, goal: int):
        # Nested loops here would probably be inefficient, so here's what's going on:
        # First, we'll add stuff until it's too big, then we cut off stuff from the beginning until
        # it isn't too big anymore, then we add on to it, then cut stuff off, etc. etc.
        current_start = 0
        current_sum = 0
        for i in range(len(self.numbers)):
            current_sum += self.numbers[i]
            while current_sum > goal:
                current_sum -= self.numbers[current_start]
                current_start += 1
            if current_sum == goal:
                return self.get_weakness_from_cont_range(current_start, i)
        # If we made it here, that's probably bad
        print("Failed to find any result!")
        return None


def parse_input(filename) -> XMAS:
    numbers = []
    with open(filename, "r") as file:
        for line in file:
            numbers.append(int(line.strip()))
    # Keep in mind that the example input uses a different preamble size than the real input, and this information
    # is not present in the input file, so this must be changed manually if switching between test and real input.
    return XMAS(numbers, 25)


# I'm not entirely convinced there's a good name for step 1 vs. step 2.
def find_weakness_step_1(xmas: XMAS) -> int:
    for i in range(xmas.start_index, len(xmas.numbers)):
        if not xmas.validate(i):
            return xmas.numbers[i]
    raise RuntimeError("Step 1: Failed to find a weakness.")


def find_weakness_step_2(xmas: XMAS, step1_result: int) -> int:
    print("Part 2: ", end="")
    return xmas.cont_range(step1_result)


def main(input_filename: str):
    start_time = time.time()
    xmas = parse_input(input_filename)

    part1_start = time.time()
    step1_result = find_weakness_step_1(xmas)
    print("Part 1: The first number in the list that isn't the sum of the past "
          f"{xmas.preamble_size} numbers is {step1_result}.")
    part2_start = time.time()
    result = find_weakness_step_2(xmas, step1_result)
    print(f"The XMAS weakness is {result}.")

    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2020/day09.txt")

    run_main()
