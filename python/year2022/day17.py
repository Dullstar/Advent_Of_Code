import time
import os
import enum


class Tile(enum.IntEnum):
    Empty = 0
    Filled = 1


Rock0 = [[Tile.Filled, Tile.Filled, Tile.Filled, Tile.Filled]]
Rock1 = [[Tile.Empty, Tile.Filled, Tile.Empty],
         [Tile.Filled, Tile.Filled, Tile.Filled],
         [Tile.Empty, Tile.Filled, Tile.Empty]]
Rock2 = [[Tile.Filled, Tile.Filled, Tile.Filled],
         [Tile.Empty, Tile.Empty, Tile.Filled],
         [Tile.Empty, Tile.Empty, Tile.Filled]]
Rock3 = [[Tile.Filled], [Tile.Filled], [Tile.Filled], [Tile.Filled]]
Rock4 = [[Tile.Filled, Tile.Filled],
         [Tile.Filled, Tile.Filled]]

Rocks = [Rock0, Rock1, Rock2, Rock3, Rock4]


# Not the same as the layouts we've seen so far.
# Designed to add more height later, so y=0 is the *floor*.
class Layout:
    def __init__(self, size_x):
        self.layout = []
        self.size_x = size_x
        self.size_y = 0

    def add_row(self):
        self.size_y += 1
        self.layout.append([Tile.Empty for _ in range(self.size_x)])

    def move_rock(self, rock_id, rock_x, rock_y, dx, dy):
        # print(dx, dy)
        rock = Rocks[rock_id]
        rock_x = rock_x + dx
        rock_y = rock_y + dy
        for y, row in enumerate(rock):
            for x, col in enumerate(row):
                if rock[y][x] == Tile.Empty:
                    continue
                nx = x + rock_x
                ny = y + rock_y
                # Somewhat awkward conditional sandwich
                if nx >= self.size_x or nx < 0 or ny < 0:
                    # print("\treturn: ", (False, rock_x - dx, rock_y - dy))
                    return False, rock_x - dx, rock_y - dy
                if ny >= self.size_y:
                    continue
                if self.layout[ny][nx] == Tile.Filled:
                    # print("\treturn 2: ", (False, rock_x - dx, rock_y - dy))
                    return False, rock_x - dx, rock_y - dy
        # print("\treturn 3: ", (True, rock_x, rock_y))
        return True, rock_x, rock_y

    def spawn_rock(self):
        # print("Spawn rock:", (2, self.size_y + 3))
        return 2, self.size_y + 3

    def place_rock(self, rock_id, rock_x, rock_y):
        # print("place")
        rock = Rocks[rock_id]
        for y, row in enumerate(rock):
            for x, col in enumerate(row):
                nx = x + rock_x
                ny = y + rock_y
                if ny >= self.size_y:
                    self.add_row()
                if rock[y][x] == Tile.Filled:
                    self.layout[ny][nx] = rock[y][x]

    def process_rocks(self, quantity, jets):
        active_rock = False
        rock_x, rock_y, rock_id = -1, -1, -1
        i = 0
        j = 0
        pt2_stash = []
        while i < quantity:
            if not active_rock:
                rock_x, rock_y = self.spawn_rock()
                rock_id = i % 5
                active_rock = True
            assert jets[j % len(jets)] == ">" or jets[j % len(jets)] == "<"
            jet_dir = 1 if jets[j % len(jets)] == ">" else -1
            rock_x, rock_y = self.move_rock(rock_id, rock_x, rock_y, jet_dir, 0)[1:]
            fell, rock_x, rock_y = self.move_rock(rock_id, rock_x, rock_y, 0, -1)
            if not fell:
                initial_y = self.size_y
                self.place_rock(rock_id, rock_x, rock_y)
                # print(self)
                # print()
                active_rock = False
                pt2_stash.append(self.size_y - initial_y)  # final - initial
                i += 1
            j += 1
        return pt2_stash  # We don't need to return the answer because we can just query it...

    def __repr__(self):
        output = ""
        for y in reversed(self.layout):
            output += "|"
            for x in y:
                output += "#" if x == Tile.Filled else "."
            output += "|\n"
        output += "+" + ("-" * self.size_x) + "+"
        with open("d17output2.txt", "w") as file:
            file.write(output)
        return output


def parse_input(filename: str):
    with open(filename, "r") as file:
        return file.read().strip()


def main(input_filename: str):
    jets = parse_input(input_filename)
    # jets = parse_input(input_filename)
    layout = Layout(7)
    pt2_stash = layout.process_rocks(2022, jets)
    # print(layout)
    # with open("pt2_stash.txt", "w") as file:
    #     file.write(f"{pt2_stash}")
    print(f"Part 1: {layout.size_y}")
    # print(pt2_stash)

    # Part 2 is a hand solve!
    return -1


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2022/day17.txt")

    run_main()
