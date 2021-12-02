import time
import os
import re


class Bag:
    def __init__(self, line):
        line = line.strip().split(" contain ")
        line[1] = line[1].strip(".").split(", ")
        self.contents = {}
        for item in line[1]:
            # Grab that number out in front
            regex = re.compile(r"[0-9]+")
            # If we didn't find one that means it's no bags inside
            if match := regex.match(item):
                quantity = int(item[match.span()[0]:match.span()[1]])
                # The +1 deals with the space
                bag_type = item[match.span()[1] + 1:]
                if quantity > 1:
                    # This gets rid of the s if it's plural
                    bag_type = bag_type[:-1]

                self.contents[bag_type] = quantity
        # Remove the s, because it's simpler if we don't need to care about singular vs. plural
        self.type = line[0][:-1]

    def contains(self, bag_type: str, bag_dict: dict):
        if bag_type in self.contents:
            return True
        else:
            for bag in self.contents:
                if bag_dict[bag].contains(bag_type, bag_dict):
                    return True
            return False

    def count_internal_bags(self, bag_dict: dict):
        internal_bags = 0
        for bag in self.contents:
            # count these bags...
            internal_bags += self.contents[bag]  # recall that this value represents the quantity
            # ...and count the bags inside of it
            internal_bags += bag_dict[bag].count_internal_bags(bag_dict) * self.contents[bag]
        return internal_bags


def parse_input(filename: str):
    with open(filename, "r") as file:
        bags = {}
        for line in file:
            bag = Bag(line)
            bags[bag.type] = bag
        return bags


def main(input_filename: str):
    start_time = time.time()
    bag_dict = parse_input(input_filename)
    part1_start = time.time()
    shiny_gold = 0
    for bag_entry in bag_dict.keys():
        bag = bag_dict[bag_entry]
        if bag.contains("shiny gold bag", bag_dict):
            shiny_gold += 1
    print(f"Part 1: Found {shiny_gold} bags containing at least one shiny gold bag.")
    part2_start = time.time()
    # I find it surprising that this runs so fast that the speed cannot be measured on my current hardware
    # (consistently 0.00... ms), but I found no evidence suggesting this measurement is a bug in the time logging,
    # confirmed by adding a sleep to the function, which resulted in an increased measurement as expected.
    print(f"Part 2: A shiny gold bag contains {bag_dict['shiny gold bag'].count_internal_bags(bag_dict)} bags.")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2020/day07.txt")
