import time
import os
import collections


def parse_input(filename: str) -> (collections.Counter, dict):
    with open(filename, "r") as file:
        contents = file.read().strip().split("\n\n")
        start_material = collections.Counter()
        for i in range(len(contents[0]) - 1):
            start_material[contents[0][i:i+2]] += 1
        find_and_replace = dict()
        for rule in contents[1].split("\n"):
            rule = rule.split(" -> ")
            assert len(rule[0]) == 2
            find_and_replace[rule[0]] = (rule[0][0] + rule[1], rule[1] + rule[0][1])
        return start_material, find_and_replace, contents[0][0], contents[0][-1]


def insert(start_material: collections.Counter, rules: dict, iterations: int):
    # print("Start:", start_material)
    for iteration in range(iterations):
        new_material = collections.Counter()
        for pair, quantity in start_material.items():
            # print(pair, quantity, rules[pair])
            new_material[rules[pair][0]] += quantity
            new_material[rules[pair][1]] += quantity
        # print(f"Step {iteration + 1}: {new_material}")
        start_material = new_material
    return start_material


def count(material: collections.Counter, start: str, end: str):
    counter = collections.Counter()
    for pair, quantity in material.items():
        counter[pair[0]] += quantity
        counter[pair[1]] += quantity
    counter[start] += 1
    counter[end] += 1
    return (max(counter.values()) - min(counter.values())) // 2


def main(input_filename: str):
    start_time = time.time()
    material, rules, start, end = parse_input(input_filename)
    part1_start = time.time()
    part2_material = insert(material, rules, 10)
    print("Part 1:", count(part2_material, start, end))
    part2_start = time.time()
    print("Part 2:", count(insert(part2_material, rules, 30), start, end))  # It wants 40, but we've already done 10.
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms", end="; ")
    print(f"including part 1: {(end_time - part1_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day14.txt")
