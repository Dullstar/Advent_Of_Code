import time
import os


# There isn't actually a fishtank in this problem, but I thought it was a cute name for the container.
class Fishtank:
    RESET_TIMER = 6
    FRESH_TIMER = 8

    def __init__(self):
        self.fish = [0 for i in range(Fishtank.FRESH_TIMER + 1)]

    def process_day(self):
        fish2 = [0 for i in range(Fishtank.FRESH_TIMER + 1)]
        for i in range(len(self.fish)):
            if i == 0:
                fish2[Fishtank.FRESH_TIMER] = self.fish[0]
                fish2[Fishtank.RESET_TIMER] += self.fish[0]
            else:
                fish2[i - 1] += self.fish[i]
        self.fish = fish2

    def __str__(self):
        output = "["
        for i in range(len(self.fish)):
            output += f"{self.fish[i]} @ {i} days; "
        output += "]"
        return output


def parse_input(filename: str) -> Fishtank:
    fishtank = Fishtank()
    with open(filename, "r") as file:
        for i in file.read().strip().split(","):
            fishtank.fish[int(i)] += 1
    return fishtank


def main(input_filename: str):
    part2_start = None  # This line exists solely to supress an incorrect Pycharm warning.
    start_time = time.time()
    fishtank = parse_input(input_filename)
    part1_start = time.time()
    for day in range(256):
        fishtank.process_day()
        if day == 79:  # actually day 80, but the variable started from 0.
            print(f"Part 1: {sum(fishtank.fish)} Lanternfish")
            part2_start = time.time()
    print(f"Part 2: {sum(fishtank.fish)} Lanternfish (breeding like rabbits!)")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms", end="; ")
    print(f"including part 1: {(end_time - part1_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day06.txt")
