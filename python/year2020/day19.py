import time
import os
import re
import time


def parse_input(filename: str, part_num: int = 1):
    with open(filename) as file:
        contents = file.read().strip().split("\n\n")
    rules_ls = contents[0].split("\n")
    known = {}
    rules = {}
    for i, rule in enumerate(rules_ls):
        rule = rule.split(": ")
        rules[rule[0]] = rule[1]

    regex = re.compile(r"[a-zA-Z]")
    for key, rule in rules.items():
        match = regex.search(rule)
        if match:
            known[key] = match.group(0)
            rules[key] = match.group(0)

    if part_num == 2:
        rules["8"] = "42 | 42 8"
        rules["11"] = "42 31 | 42 11 31"
        for i in range(3):
            # Credit to KBD2 on the OneLoneCoder discord for this loop; the thing I was trying to do wouldn't work;
            # they literally wrote these four lines for me, and that made the rest of the code start working, so I'd
            # say that definitely deserves some credit!

            # Further inspection in 2021: This hardcoding of the possible depth as suggested by KBD2 is probably what
            # is meant by the hint regarding only needing to "Remember, you only need to handle the rules you have;
            # building a solution that could handle any hypothetical combination of rules would be significantly more
            # difficult." However, I don't know a trivial way to prove 3 is sufficient, particularly for all possible
            # inputs for the day. If you're running this yourself, and the script does not return a correct answer
            # for part 2, try increasing this number.
            rules["8"] = rules["8"].replace("8", "(" + rules["8"] + ")")
            rules["11"] = rules["11"].replace("11", "(" + rules["11"] + ")")
        rules["8"] = rules["8"].replace("8", "")
        rules["11"] = rules["11"].replace("11", "")

    find_nums = re.compile(r"[0-9]")
    while len(known) < len(rules):
        new_known = {}
        for rule_regex, rule_string in known.items():
            rule_regex = re.compile(fr"\b{rule_regex}\b")
            for key, rule in rules.items():
                # Update the rule with new information
                rule = rule_regex.sub(f"(?:{rule_string})", rule)
                rules[key] = rule
                # Check if this rule is finished yet
                match = find_nums.search(rule)
                if match is None:
                    rule = re.sub(r" ", "", rule)
                    new_known[key] = rule
                    rules[key] = rule
        known = new_known

    return rules, contents[1].split("\n")


def main(input_filename: str):
    start_time = time.time()
    rules, messages = parse_input(input_filename, 1)

    # print(rules["0"])
    part1_start = time.time()
    total = 0
    rule_regex = re.compile(rules["0"])
    for message in messages:
        match = rule_regex.match(message)
        if match and len(match.group(0)) == len(message):
            total += 1
    print(f"Part 1: {total} valid messages")

    part2_parse = time.time()
    rules, messages = parse_input(input_filename, 2)
    part2_start = time.time()
    # print(rules["0"])
    total = 0
    rule_regex = re.compile(rules["0"])
    for message in messages:
        match = rule_regex.match(message)
        if match and len(match.group(0)) == len(message):
            total += 1
    print(f"Part 2: {total} valid messages")

    end_time = time.time()
    print("Elapsed Time:")
    # print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_parse - start_time) * 1000:.2f} ms", end="; ")
    print(f"Parsing: {(part1_start - start_time) * 1000:.2f} ms", end="; ")
    print(f"Evaluation: {(part2_parse - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_parse) * 1000:.2f} ms", end="; ")
    print(f"Parsing: {(part2_start - part2_parse) * 1000:.2f} ms", end="; ")
    print(f"Evaluation: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2020/day19.txt")
