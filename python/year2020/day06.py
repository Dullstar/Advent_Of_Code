import time
import os


def parse_input(filename):
    with open(filename, "r") as file:
        raw_contents = file.read()
        groups = raw_contents.strip().split("\n\n")
    return groups


def get_unique_answers(group: str):
    encountered = dict()
    for char in group:
        if char != "\n":
            encountered[char] = True
    result = 0
    for key in encountered.keys():
        result += 1
    return result


# I thought this was a clever idea that would avoid a dictionary and hopefully be faster.
# It wasn't (at least not for an input of this size), but I wanted to save the idea for later,
# particularly as I suspect it might be more useful in, for example, C/C++.
# def get_unique_answers(group: str):
#     encountered = [False for i in range(26)]
#     for char in group:
#         c = char.encode()[0]
#         if c != 10:
#             encountered[c - 97] = True
#     result = 0
#     for item in encountered:
#         result += item
#     return result


def get_shared_answers(group: str):
    sets = []
    for individual in group.split("\n"):
        # We convert each individual's response into a set...
        sets.append({a for a in individual})
    # ...then we take all of those sets and get the intersection, i.e. the elements common to all of them
    # (with this wonky syntax, because the only function I saw that does this is a member function of set).
    # ideally, I'd want a standalone intersection(*sets) but that doesn't seem to exist unless I just didn't see it.
    return len(sets[0].intersection(*sets[1:]))


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    start_time = time.time()
    groups = parse_input(input_filename)
    unique_answers = 0
    shared_answers = 0

    part1_start = time.time()
    for group in groups:
        unique_answers += get_unique_answers(group)

    part2_start = time.time()
    for group in groups:
        shared_answers += get_shared_answers(group)
    end_time = time.time()

    print(f"Unique answers per group: {unique_answers}")
    print(f"Shared answers per group: {shared_answers}")

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2020/day06.txt"
        main(filename)

    run_main()
