import time
import os
import re


class Status:
    KEEP_GOING = 0
    WORKS = 1
    OVERSHOT = 2


class Probe:
    def __init__(self, vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.x = 0
        self.y = 0
        self.max_y = 0
        self.current_step = 0

    def step(self):
        self.x, self.vel_x = self.move_x(self.x, self.vel_x)
        self.y, self.vel_y = self.move_y(self.y, self.vel_y)
        self.current_step += 1
        if self.y > self.max_y:
            self.max_y = self.y

    def check(self, target_x_min, target_x_max, target_y_min, target_y_max):
        if (self.x >= target_x_min) and (self.x <= target_x_max) \
                and (self.y >= target_y_min) and (self.y <= target_y_max):
            return Status.WORKS
        if (self.x > target_x_max) or (self.y < target_y_min):
            return Status.OVERSHOT
        return Status.KEEP_GOING

    def try_probe(self, target_x_min, target_x_max, target_y_min, target_y_max):
        while True:
            self.step()
            result = self.check(target_x_min, target_x_max, target_y_min, target_y_max)
            if result == Status.OVERSHOT:
                return False,
            elif result == Status.WORKS:
                return True, self.max_y, self.current_step

    @staticmethod
    def move_x(pos_x: int, vel_x: int):
        pos_x += vel_x
        if vel_x != 0:
            vel_x += (-1 if vel_x > 0 else 1)
        return pos_x, vel_x

    @staticmethod
    def move_y(pos_y: int, vel_y: int):
        pos_y += vel_y
        vel_y -= 1
        return pos_y, vel_y


def find_valid_x(target_x_min: int, target_x_max: int):
    valid = set()
    for vel_x in range(0, target_x_max + 1):
        init_vel_x = vel_x
        pos_x = 0
        step = 0
        while pos_x < target_x_max:
            step += 1
            pos_x, vel_x = Probe.move_x(pos_x, vel_x)
            if (pos_x >= target_x_min) and (pos_x <= target_x_max):
                valid.add(init_vel_x)
            if vel_x == 0:
                break
    return list(valid)


def find_valid_y(target_y_min: int, target_y_max: int):
    valid = set()
    for vel_y in range(target_y_min, abs(target_y_min) + 1):
        step = 0
        init_vel_y = vel_y
        pos_y = 0
        while pos_y > target_y_min:
            step += 1
            pos_y, vel_y = Probe.move_y(pos_y, vel_y)
            if (pos_y <= target_y_max) and (pos_y >= target_y_min):
                valid.add(init_vel_y)
    return list(valid)


def try_probes(target_x_min, target_x_max, target_y_min, target_y_max, valid_x, valid_y):
    max_range = 0
    total = 0
    for vel_y in valid_y:
        for vel_x in valid_x:
            probe = Probe(vel_x, vel_y)
            result = probe.try_probe(target_x_min, target_x_max, target_y_min, target_y_max)
            if result[0]:
                total += 1
                if result[1] > max_range:
                    max_range = result[1]
    return max_range, total


def parse_input(filename: str):
    with open(filename, "r") as file:
        contents = file.read().strip()
    regex = re.compile(r"x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)")
    match = regex.search(contents)
    target_x_min = int(match[1])
    target_x_max = int(match[2])
    target_y_min = int(match[3])
    target_y_max = int(match[4])
    if target_x_max < target_x_min:
        target_x_max, target_x_min = target_x_min, target_x_max
    if target_y_max < target_y_min:
        target_y_max, target_y_min = target_y_min, target_y_max
    assert target_x_max > 0 and target_x_min > 0, "Uh oh, I made a bad assumption about the input file!"
    assert target_y_max < 0 and target_y_min < 0, "Uh oh, I made a bad assumption about the input file!"
    return target_x_min, target_x_max, target_y_min, target_y_max


def main(input_filename: str):
    start_time = time.time()
    target_x_min, target_x_max, target_y_min, target_y_max = parse_input(input_filename)
    part1_start = time.time()
    valid_x = find_valid_x(target_x_min, target_x_max)
    valid_y = find_valid_y(target_y_min, target_y_max)
    results = try_probes(target_x_min, target_x_max, target_y_min, target_y_max, valid_x, valid_y)
    end_time = time.time()
    print(f"Part 1: The highest trick shot reaches y = {results[0]}")
    print(f"Part 2: There are {results[1]} possible trajectories")
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1 + Part 2: {(end_time - part1_start) * 1000:.2f} ms (evaluation is combined today)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day17.txt")
