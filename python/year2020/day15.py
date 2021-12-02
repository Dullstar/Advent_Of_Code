import time
import os


# This one is very slow.
# Things that have been tried and did *not* work:
#  - What if we just use a really big list?
#  - Using the arrays in the array module?
# It didn't save significant time on Part 2, and most if not all of the savings were eaten up by slower initialization.
# In C++, std::vector seems like it should be equivalent to using the array module... and there, we get really fast
# runtimes, and it's STILL significantly faster even with optimizations off - so Python's overhead would necessitate
# a completely different approach to fix this, I think.

class MemGame:
    def __init__(self, numbers: list):
        self.memory = {}
        self.turn_count = 1
        for number in numbers:
            self.memory[number] = self.turn_count
            self.previous_num = number
            self.turn_count += 1
        del self.memory[self.previous_num]  # Don't want to remember the last value quite yet
        # print(self.memory)

    def process_turn(self):
        previous_turn = self.turn_count - 1
        if self.previous_num in self.memory:
            _next = previous_turn - self.memory[self.previous_num]
        else:
            _next = 0

        self.memory[self.previous_num] = previous_turn
        self.turn_count += 1
        self.previous_num = _next

    def process_to(self, stop: int):
        """Note: the stop condition works the same way slices do, so to go up to and including 2020, set stop to 2021"""
        while self.turn_count < stop:
            self.process_turn()
        print(f"Turn {self.turn_count - 1}: {self.previous_num}")


def parse_input(filename) -> MemGame:
    with open(filename, "r") as file:
        return MemGame([int(i) for i in file.read().strip().split(",")])


def main(input_filename: str):
    start_time = time.time()
    # Consider returning game directly from parse_input without the go between.
    game = parse_input(input_filename)
    part1_start = time.time()
    print("Part 1: ", end="")
    game.process_to(2021)
    part2_start = time.time()
    print("Part 2 (this may take a while): ", end="")
    game.process_to(30000001)
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms ({(end_time - part2_start):.2f} s)", end="; ")
    print(f"including part 1: {(end_time - part1_start) * 1000:.2f} ms ({(end_time - part1_start):.2f} s)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms ({(end_time - start_time):.2f} s)")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2020/day15.txt")

    run_main()
