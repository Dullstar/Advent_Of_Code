import time
import os
import itertools
import collections.abc  # honestly, not really needed: it's just here for a type hint.
import collections  # code runs fine with just collections.abc, but it causes PyCharm warnings in parse_input

Segment = {
    "a": 0b_0000_0001,
    "b": 0b_0000_0010,
    "c": 0b_0000_0100,
    "d": 0b_0000_1000,
    "e": 0b_0001_0000,
    "f": 0b_0010_0000,
    "g": 0b_0100_0000
}


class Digit:
    num = [
        Segment["a"] | Segment["b"] | Segment["c"] | Segment["e"] | Segment["f"] | Segment["g"],
        Segment["c"] | Segment["f"],
        Segment["a"] | Segment["c"] | Segment["d"] | Segment["e"] | Segment["g"],
        Segment["a"] | Segment["c"] | Segment["d"] | Segment["f"] | Segment["g"],
        Segment["b"] | Segment["c"] | Segment["d"] | Segment["f"],
        Segment["a"] | Segment["b"] | Segment["d"] | Segment["f"] | Segment["g"],
        Segment["a"] | Segment["b"] | Segment["d"] | Segment["e"] | Segment["f"] | Segment["g"],
        Segment["a"] | Segment["c"] | Segment["f"],
        Segment["a"] | Segment["b"] | Segment["c"] | Segment["d"] | Segment["e"] | Segment["f"] | Segment["g"],
        Segment["a"] | Segment["b"] | Segment["c"] | Segment["d"] | Segment["f"] | Segment["g"]
    ]

    # len used for consistency with len()
    len_segments = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]


class MysteryDisplay:
    def __init__(self):
        self.num: list[int] = [0 for i in range(10)]
        self.num_string: list[str or None] = [None for i in range(10)]
        self.orig_num_string: list[str or None] = [None for i in range(10)]
        self.seg = {
            "a": 0,
            "b": 0,
            "c": 0,
            "d": 0,
            "e": 0,
            "f": 0,
            "g": 0
        }

    def set_numbers(self):
        for i, sequence in enumerate(self.orig_num_string):
            for char in sequence:
                self.num[i] |= self.seg[char]

    def check_numbers(self) -> bool:
        return self.num == Digit.num

    def strip_char(self, char):
        for i, s in enumerate(self.num_string):
            self.num_string[i] = s.replace(char, "")


Display = collections.namedtuple("Display", ["In", "Out"])


def parse_input(filename: str) -> list[Display]:
    display = []
    with open(filename, "r") as file:
        for line in file:
            line = line.split("|")
            display.append(Display(line[0].split(), line[1].split()))
    return display


def count_easy_digits(displays: list[Display]):
    total = 0
    for display in displays:
        for sequence in display.Out:
            if len(sequence) == Digit.len_segments[1] or len(sequence) == Digit.len_segments[4] \
                    or len(sequence) == Digit.len_segments[7] or len(sequence) == Digit.len_segments[8]:
                total += 1
    return total


def find_sum_display_outputs(displays: list[Display]):
    total = 0
    for display in displays:
        for md in guess_strings(display):
            # print("Guess")
            try:
                if (result := assign(display, md)) is not None:
                    total += result
                    break
            except:
                print(md.num_string)
                print(md.orig_num_string)
                raise
    return total


def guess_strings(display: Display) -> collections.abc.Generator[MysteryDisplay]:
    md = MysteryDisplay()
    seq5 = []
    seq6 = []
    num5 = [2, 3, 5]
    num6 = [0, 6, 9]
    for sequence in display.In:
        if len(sequence) == 5:
            seq5.append(sequence)
        elif len(sequence) == 6:
            seq6.append(sequence)
        else:
            for i in [1, 4, 7, 8]:
                if len(sequence) == Digit.len_segments[i]:
                    md.orig_num_string[i] = sequence
                    break
    assert (len(seq5) == 3) and (len(seq6) == 3)
    for n0, n1, n2 in itertools.permutations(num5):
        md.orig_num_string[n0] = seq5[0]
        md.orig_num_string[n1] = seq5[1]
        md.orig_num_string[n2] = seq5[2]
        for m0, m1, m2 in itertools.permutations(num6):
            md.orig_num_string[m0] = seq6[0]
            md.orig_num_string[m1] = seq6[1]
            md.orig_num_string[m2] = seq6[2]
            md.num_string = [i for i in md.orig_num_string]
            md.num = [0 for i in range(10)]
            yield md


def assign(display: Display, md: MysteryDisplay):
    """Based on the given MysteryDisplay, work out what the settings are and return the output number from the display.
    guess_strings can provide the strings if you don't know them - this will then test them, basically by solving it as
    if those settings are correct, then sanity checking the result - if the strings aren't assigned correctly, then
    it'll fail the sanity check and return None."""

    # Identifying the 6 segment pieces is easy: compare to 8 and see what's missing.
    to_remove = []
    for char in md.num_string[8]:
        if char not in md.num_string[0]:
            md.seg[char] = Segment["d"]
            to_remove.append(char)
        elif char not in md.num_string[6]:
            md.seg[char] = Segment["c"]
            to_remove.append(char)
        elif char not in md.num_string[9]:
            md.seg[char] = Segment["e"]
            to_remove.append(char)
    # Get rid of these so we can focus only on ones we still need to identify
    for char in to_remove:
        md.strip_char(char)

    # This should leave 1 with only 1 char, which is F
    def handle_1_left(num: int, label: str):
        assert(len(md.num_string[num]) == 1)
        md.seg[md.num_string[num]] = Segment[label]
        md.strip_char(md.num_string[num])
    handle_1_left(1, "f")

    # ...which leaves 7 with only 1, which is A
    handle_1_left(7, "a")

    # ...leaving 4 with just B
    handle_1_left(4, "b")

    # and then we know the last one by process of elimination, so just look at anything that has it
    handle_1_left(8, "g")

    md.set_numbers()
    if md.check_numbers():
        # This feels a little janky but it works
        numstring = ""
        for sequence in display.Out:
            digit = 0
            for char in sequence:
                digit |= md.seg[char]
            for n in range(10):
                if Digit.num[n] == digit:
                    numstring += str(n)
        return int(numstring)
    return None


def main(input_filename: str):
    start_time = time.time()
    displays = parse_input(input_filename)
    part1_start = time.time()
    print(f"Part 1: {count_easy_digits(displays)} occurrences of 1, 4, 7, or 8")
    part2_start = time.time()
    print(f"Part 2: Corrected displays sum to {find_sum_display_outputs(displays)}")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day08.txt")
