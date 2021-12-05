import time
import os
# import collections


# TODO: Check if there's something like this that's mutable.
# Number = collections.namedtuple("Number", ["number", "called"])
class Number:
    def __init__(self, number: int, called: bool):
        self.number: int = number
        self.called: bool = called


class Bingo:
    def __init__(self, as_string: str):
        self.contents = [Number(int(i), False) for i in as_string.split()]
        self.lookup = dict()
        self.won = False  # used to prevent double wins
        for y in range(5):
            for x in range(5):
                self.lookup[self[x, y].number] = x, y

    def __getitem__(self, key: tuple[int, int]):
        # x, y = key  # contents of key
        return self.contents[key[0] + (key[1] * 5)]

    # Was used during development to confirm cards loaded properly. It's being left in case a verbose output mode
    # is introduced in the future.
    def __str__(self):
        i = 0
        output = ""
        for num in self.contents:
            output += f"{num.number:2} "
            i += 1
            if i > 4:
                output += "\n"
                i = 0
        return output

    # Returns True if and only if marking off results in a bingo; doesn't tell you if the number's in there.
    def mark(self, number: int) -> bool:
        if number in self.lookup:
            self[self.lookup[number]].called = True
        if self.check_for_bingo():
            self.won = True
            return True
        return False

    def check_for_bingo(self) -> bool:
        if self.won:  # Don't need to check again if we've already won
            return False
        # Check horizontals
        for y in range(5):
            broke = False
            for x in range(5):
                if not self[x, y].called:
                    broke = True
                    break
            if not broke:
                return True

        # Check verticles:
        for x in range(5):
            broke = False
            for y in range(5):
                if not self[x, y].called:
                    broke = True
                    break
            if not broke:
                return True
        # Diagonals don't need to be checked.
        return False

    def score(self, multiplier: int):
        total = 0
        for item in self.contents:
            if not item.called:
                total += item.number
        return total * multiplier


def parse_input(filename: str) -> (list[Bingo], list[int]):
    with open(filename, "r") as file:
        contents = file.read().split("\n\n")
        bingo_calls = [int(i) for i in contents[0].split(",")]
        bingo_cards = [Bingo(card) for card in contents[1:]]
    return bingo_calls, bingo_cards


def main(input_filename: str):
    start_time = time.time()
    bingo_calls, bingo_cards = parse_input(input_filename)
    part1_start = time.time()
    scores = []
    for call in bingo_calls:
        for card in bingo_cards:
            if card.mark(call):  # means there was a bingo
                scores.append(card.score(call))
    end_time = time.time()

    print(f"Part 1: Your score is: {scores[0]}")
    print(f"Part 2: Your score is: {scores[-1]}")

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1 + Part 2: {(end_time - part1_start) * 1000:.2f} ms (evaluation is combined today)")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day04.txt")
