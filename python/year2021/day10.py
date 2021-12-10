import time
import os
import collections


def check_line(line: str):
    stack = collections.deque()
    opening = {"(": 1, "[": 2, "{": 3, "<": 4}
    closing = {")": ("(", 3), "]": ("[", 57), "}": ("{", 1197), ">": ("<", 25137)}
    for i, char in enumerate(line):
        if char in opening:
            stack.append(char)
        else:
            popped = stack.pop()
            if closing[char][0] != popped:
                return closing[char][1], 0
    line_score = 0
    while len(stack) > 0:
        line_score *= 5
        popped = stack.pop()
        line_score += opening[popped]
    return 0, line_score


def check_all_lines(lines: list[str]):
    corrupt_score = 0
    completion_score = []
    for line in lines:
        line_result = check_line(line)
        corrupt_score += line_result[0]
        if line_result[1] != 0:
            completion_score.append(line_result[1])

    return corrupt_score, sorted(completion_score)[len(completion_score) // 2]


def parse_input(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return [line.strip() for line in file]


def main(input_filename: str):
    start_time = time.time()
    lines = parse_input(input_filename)
    part1_start = time.time()
    corrupt_score, completion_score = check_all_lines(lines)
    end_time = time.time()
    print(f"Part 1: Corruption score: {corrupt_score}")
    print(f"Part 2: Completion score: {completion_score}")
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1 + Part 2: {(end_time - part1_start) * 1000:.2f} ms (evaluation is combined today)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day10.txt")
