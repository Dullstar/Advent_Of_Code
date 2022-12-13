import time
import json
import os
from collections import namedtuple


Pair = namedtuple("Pair", "first second")


# The return values for this function follow C's strcmp conventions: -1 for less than, 0 for equal, 1 for greater than
# Since I didn't end up sorting for Part 2 we could have used a bool, but it was janky because the recursion needs to
# know the difference between greater than/less than (we're done), return the result and equal (keep going), and None
# feels weird in this situation; plus, with this convention, we are ABLE to use this function with functools.cmp_to_key
# for use with sorting built-ins.
def packet_pair_cmp(p: Pair) -> int:
    for i, item in enumerate(p.first):
        if i >= len(p.second):
            return 1
        first = item
        second = p.second[i]
        if type(first) != type(second):
            if type(first) == int:
                first = [first]
            elif type(second) == int:
                second = [second]
        if first == second:
            # If they are the same, it's too early to tell and we need to keep going. The remainder of the loop assumes
            # that first != second and it WILL produce incorrect results if they're equal, so we need to skip it!
            # (list comparisons will need to account for the possibilty of stuff like 9,[10] vs. [9],10)
            continue
        if type(first) == int:
            return -1 if first < second else 1
        elif type(first) == list:
            temp = packet_pair_cmp(Pair(first, second))
            if temp == 0:
                continue  # If they're equal (return value of None) then we must keep going.
            return temp
    # 0 return value should only happen if we've got something that should be considered equal but isn't technically
    # ==, such as 9,[10] and [9],10.
    return -1 if len(p.first) < len(p.second) else 0


def find_correctly_ordered_pairs(packet_pairs: list[Pair]):
    good = []
    for i, packet_pair in enumerate(packet_pairs):
        if packet_pair_cmp(packet_pair) == -1:  # -1 -> less than
            good.append(i + 1)
    return good


def find_decoder_key_components(packets: list):
    n1 = 1  # this accounts for the 1-index
    n2 = 2  # and this accounts for the fact that [[2]] will definitely be behind it.
    for packet in packets:
        if packet_pair_cmp(Pair(packet, [[2]])) == -1:
            n1 += 1
            n2 += 1
        elif packet_pair_cmp(Pair(packet, [[6]])) == -1:
            n2 += 1
    return n1, n2


def parse_input(filename: str):
    packet_pairs = []
    packets = []  # [[[2]], [[6]]]
    with open(filename, "r") as file:
        contents = file.read().strip().split("\n\n")
        for item in contents:
            item = item.split("\n")
            assert len(item) == 2
            first = json.loads(item[0])
            second = json.loads(item[1])
            packets.append(first)
            packets.append(second)
            packet_pairs.append(Pair(first, second))
    return packet_pairs, packets


def main(input_filename: str):
    start_time = time.time()
    packet_pairs, packets = parse_input(input_filename)
    part1_start = time.time()
    correct = find_correctly_ordered_pairs(packet_pairs)
    print(f"Part 1: Sum of correct indices: {sum(correct)}")

    part2_start = time.time()
    n1, n2 = find_decoder_key_components(packets)
    print(f"Part 2: The decoder key is: {n1} * {n2} = {n1 * n2}")
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day13.txt")

    run_main()
