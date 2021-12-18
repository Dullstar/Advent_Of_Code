import time
import os
import itertools

# Definitely an example of "This works."
# I wouldn't necessarily say this is *good*.

# Biggest improvements I can think of:
# Improve adding's interaction with nest_level tracking
#   (and hopefully remove that SnailfishNumber -> str -> SnailfishNumber chain in the process)
# Remove eval() because I don't like trusting user input quite that much
# Can we make traverse work with an iterator so we could just use a simple for loop?
#   (with the current design lhs and rhs probably get in the way, but still, it's something to look into)


class RefInt:
    """A wrapper class around int so we can have a reference. AFAIK there's no other way to force it to pass an
    integer by reference and not by value... but maybe there is and I just don't know about it. """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    # Defining this saves some type checking - lets us just call the magnitude on SnailfishNumbers or RefInts without
    # having to check which one we're dealing with.
    def magnitude(self):
        return self.value


class SnailfishNumber:
    def __init__(self, lhs: int or SnailfishNumber, rhs: int or SnailfishNumber, nest_level: int = 0):
        self.lhs = lhs if type(lhs) == SnailfishNumber else RefInt(lhs)
        self.rhs = rhs if type(rhs) == SnailfishNumber else RefInt(rhs)
        self.nest_level = nest_level

    def __add__(self, other):
        # Doing it this way is extremely likely to be ineffecient, but it does fix the nest levels in a
        # convenient manner.
        return parse_snailfish_number(f"[{self}, {other}]")

    def __str__(self):
        return f"[{self.lhs}, {self.rhs}]"  # <{self.nest_level}>]"

    def reduce(self):
        while True:
            if not self.explode():
                if not self.split():
                    return

    # There's been a few warnings in here about unresolved references, but they're incorrect, so I silenced them
    # noinspection PyUnresolvedReferences
    def explode(self):
        # Figure out what is next to what
        number_map = []
        to_explode: None or tuple[int, int] = None

        def traverse(num: SnailfishNumber):
            nonlocal number_map, to_explode
            if type(num.lhs) == SnailfishNumber:
                # Assumption: Not possible for more levels of nesting to occur.
                number_map.append(None)
                traverse(num.lhs)
                if to_explode is None and num.lhs.nest_level == 4:
                    to_explode = len(number_map) - 2, len(number_map) - 1
                    num.lhs = RefInt(0)
            else:
                number_map.append(num.lhs)
            if type(num.rhs) == SnailfishNumber:
                number_map.append(None)
                traverse(num.rhs)
                if to_explode is None and num.rhs.nest_level == 4:
                    to_explode = len(number_map) - 2, len(number_map) - 1
                    num.rhs = RefInt(0)
            else:
                number_map.append(num.rhs)
        traverse(self)
        # print(number_map)
        # print(to_explode)
        if to_explode is None:
            return False
        # Pycharm doesn't like this None or tuple structure, it seems.
        for i in range(to_explode[0] - 1, -1, -1):
            if number_map[i] is not None:
                # print(f"Editing: {i} (first loop)")
                number_map[i].value += number_map[to_explode[0]].value
                break
        for i in range(to_explode[1] + 1, len(number_map)):
            if number_map[i] is not None:
                # print(f"Editing: {i} (second loop)")
                number_map[i].value += number_map[to_explode[1]].value
                break
        return True

    def split(self):
        def traverse(num: SnailfishNumber):
            # print("Called traverse: Num is: ", num)
            assert type(num) == SnailfishNumber
            if type(num.lhs) == RefInt and num.lhs.value >= 10:
                num.lhs = SnailfishNumber(num.lhs.value // 2,
                                          (num.lhs.value // 2) + (num.lhs.value % 2),
                                          num.nest_level + 1)
                return True
            if type(num.lhs) == SnailfishNumber and traverse(num.lhs):
                return True
            if type(num.rhs) == RefInt and num.rhs.value >= 10:
                num.rhs = SnailfishNumber(num.rhs.value // 2,
                                          (num.rhs.value // 2) + (num.rhs.value % 2),
                                          num.nest_level + 1)
                return True
            if type(num.rhs) == RefInt:
                return False
            return traverse(num.rhs)
        return traverse(self)

    def magnitude(self):
        return (3 * self.lhs.magnitude()) + (2 * self.rhs.magnitude())


def parse_snailfish_number(line):
    _raw = eval(line)
    assert len(_raw) == 2

    def create_num(raw: int or list, nest_level: int = 0):
        lhs = raw[0] if type(raw[0]) == int else create_num(raw[0], nest_level + 1)
        rhs = raw[1] if type(raw[1]) == int else create_num(raw[1], nest_level + 1)
        return SnailfishNumber(lhs, rhs, nest_level)
    return create_num(_raw)


def parse_input(filename: str):
    snailfish_numbers = []
    with open(filename, "r") as file:
        for line in file:
            snailfish_numbers.append(parse_snailfish_number(line))
    return snailfish_numbers


def main(input_filename: str):
    start_time = time.time()
    snailfish_nums = parse_input(input_filename)

    part1_start = time.time()
    total = snailfish_nums[0]
    for num in snailfish_nums[1:]:
        total += num
        total.reduce()
    print(f"Part 1: The magnitude of the full sum is {total.magnitude()}")

    part2_start = time.time()
    magnitudes = []
    for i, j in itertools.permutations(range(len(snailfish_nums)), 2):
        result = snailfish_nums[i] + snailfish_nums[j]
        result.reduce()
        magnitudes.append(result.magnitude())
    print(f"Part 2: The highest possible magnitude from summing two is {max(magnitudes)}")

    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day18.txt")
