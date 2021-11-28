import time
import os
import re
import enum
import sys
import queue as q


# -- START TILES SUBSECTION -- #
# (This section was once its own file in the original repository)
# At a certain point, Day 20 transitioned from, "Let's do this well!" to "Just get it done..."
# Here is where the ickiness is hidden away.

class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    NORTH_FLIP = 4
    EAST_FLIP = 5
    SOUTH_FLIP = 6
    WEST_FLIP = 7


class Tile:
    def __init__(self, string_form: str):
        string_form = string_form.split("\n")
        tile_id = re.search(r"[0-9]+", string_form[0])
        self.tile_id = tile_id.group(0)
        self.width = len(string_form[1])
        self.height = len(string_form) - 1
        self.contents = []
        for t_str in string_form[1:]:
            for c in t_str:
                self.contents.append(0 if c == "." else 1)
        self.flipped = False
        self.rotation = Direction.NORTH
        self.borders = {}
        self._init_borders()
        self.location = None

    def __getitem__(self, key: tuple):
        orig_x = self.width - 1 - key[0] if self.flipped else key[0]
        orig_y = key[1]
        if self.rotation == Direction.NORTH:
            x = orig_x
            y = orig_y
        elif self.rotation == Direction.EAST:
            x = orig_y
            y = self.height - 1 - orig_x
        elif self.rotation == Direction.SOUTH:
            x = self.width - 1 - orig_x
            y = self.height - 1 - orig_y
        elif self.rotation == Direction.WEST:
            x = self.width - 1 - orig_y
            y = orig_x
        else:
            print("A tile is an an invalid state", file=sys.stderr)
            raise
        return self.contents[y * self.width + x]

    def __str__(self):
        output = ""
        output += f"Tile {self.tile_id}:\n"
        total = 0
        for c in self.contents:
            if total == self.width:
                output+="\n"
                total = 0
            output += "." if c == 0 else "#"
            total += 1
        return output

    def _init_borders(self):
        # I wanted the rotation logic to not be dependent on the width = height assumption to make it a useful guide
        # for later re-use, but the border stuff requires it now to make sense.
        if self.width != self.height:
            print(f"A tile's height ({self.height}) did not equal its width ({self.width}).", file=sys.stderr)
            raise
        # Stash the starting state here
        store_rotation = self.rotation
        store_flip = self.flipped

        directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST,
                      Direction.NORTH_FLIP, Direction.SOUTH_FLIP, Direction.EAST_FLIP, Direction.WEST_FLIP]
        for direction in directions:
            # I'm sure there's a better way.
            if direction == Direction.NORTH_FLIP:
                self.rotation = Direction.NORTH
                self.flipped = True
            elif direction == Direction.EAST_FLIP:
                self.rotation = Direction.EAST
                self.flipped = True
            elif direction == Direction.SOUTH_FLIP:
                self.rotation = Direction.SOUTH
                self.flipped = True
            elif direction == Direction.WEST_FLIP:
                self.rotation = Direction.WEST
                self.flipped = True
            else:
                self.rotation = direction
                self.flipped = False

            bin_string = ""
            for x in range(self.width):
                bin_string += str(self[x, 0])

            self.borders[direction] = int(bin_string, 2)

        # Put the starting state back
        self.rotation = store_rotation
        self.flipped = store_flip

    def place_if_border_matches(self, other):
        assert self.location is not None, "This shouldn't get called if self.location is None"
        match = None
        for self_key, self_value in self.borders.items():
            if match is not None:
                break
            for other_key, other_value in other.borders.items():
                if self_value == other_value:
                    match = self_key, other_key
                    break

        if match:
            if match[1] == Direction.NORTH_FLIP or match[1] == Direction.SOUTH_FLIP \
                    or match[1] == Direction.WEST_FLIP or match[1] == Direction.EAST_FLIP:
                other.flipped = True

            rel_location = self._find_relative_coordinates(match)
            # print("RL: ", rel_location, "SL: ", self.location)
            other.location = self.location[0] + rel_location[0], self.location[1] + rel_location[1]
            self._rotate_other(other, match)
            return True
        return False

    @staticmethod
    def _find_relative_coordinates(match: tuple[Direction, Direction]):
        # EAST and WEST flip are weird in terms of accounting.
        if match[0] == Direction.NORTH or match[0] == Direction.NORTH_FLIP:
            return 0, -1
        if match[0] == Direction.SOUTH or match[0] == Direction.SOUTH_FLIP:
            return 0, 1
        # I expected west would get -1 and east would get 1, but experimentally, we want the other way around for
        # reasons I don't fully understand. Still, it would seem we should get a working result by swapping them,
        # so that'll do.
        if match[0] == Direction.WEST or match[0] == Direction.WEST_FLIP:
            return 1, 0
        if match[0] == Direction.EAST or match[0] == Direction.EAST_FLIP:
            return -1, 0
        raise ValueError("Somehow, _find_relative_coordinates failed to find a result.")

    # Can't think of a good name for this function. Its purpose is to make things easier by rotating the entire
    # contents such that rotation can be set to north, so we won't have to account for it when figuring out where to
    # place neighboring tiles.
    def perma_rotate(self):
        new_contents = []
        for y in range(self.height):
            for x in range(self.width):
                new_contents.append(self[x, y])
        self.contents = new_contents
        self.rotation = Direction.NORTH
        self.flipped = False
        self._init_borders()

    def _rotate_other(self, other, match: tuple[Direction, Direction]):
        # This isn't a good way to do this, really. Ideally, we'd want to precompute this and then select the correct
        # option. But quite frankly I was getting confused thinking about the relative rotations, and this works well
        # enough for this problem. If this were production code we'd want to do it right, but since it's not I'll just
        # make it work.
        # print(f"Source Tile {self.tile_id}: Rotate other Tile {other.tile_id}: ", match)
        for f in [False, True]:
            other.flipped = f
            if f:
                other.perma_rotate()
            for i in range(4):
                other.rotation = Direction.EAST
                other.perma_rotate()

                # Experimentally, the FLIP directions don't seem to come up for match[0]
                # I think that's bcause of some relative stuff going on that causes other to always be flip and
                # never this one. Or maybe it's just a coincidence that could bite on specific inputs.

                # The way we've defined the flips and border directions may be easy to explain, but then it leads
                # to weirdness like this.
                if match[0] == Direction.EAST and self.borders[Direction.EAST] == other.borders[Direction.WEST_FLIP]:
                    return
                if match[0] == Direction.WEST and self.borders[Direction.WEST] == other.borders[Direction.EAST_FLIP]:
                    return
                if match[0] == Direction.SOUTH and self.borders[Direction.SOUTH] == other.borders[Direction.NORTH_FLIP]:
                    return
                if match[0] == Direction.NORTH and self.borders[Direction.NORTH] == other.borders[Direction.SOUTH_FLIP]:
                    return

        print("This shouldn't be possible to reach! The offending match value was: ", match, file=sys.stderr)
        assert False

    def _search_for_sea_monsters_subroutine(self):
        # Format: Each internal list is a y coordinate relative to origin (top left) of sea monster
        # Each number in the list is the corresponding x coordinate.
        SEA_MONSTER = [[18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]
        SEA_MONSTER_SIZE_X = 20
        SEA_MONSTER_SIZE_Y = 3

        changed = False

        def check_lines(_x: int, _y: int):
            _match_coords = []
            # Check the lines
            for sea_monster_y in range(SEA_MONSTER_SIZE_Y):
                for sea_monster_x in SEA_MONSTER[sea_monster_y]:
                    if self[sea_monster_x + _x, sea_monster_y + _y] != 1:
                        return None
                    else:
                        _match_coords.append((sea_monster_x + _x, sea_monster_y + _y))
            return _match_coords

        for y in range(self.height - (SEA_MONSTER_SIZE_Y + 1)):
            for x in range(self.width - (SEA_MONSTER_SIZE_X + 1)):
                if (match_coords := check_lines(x, y)) is not None:
                    changed = True
                    for coord in match_coords:
                        # Setting to 0 allows us to get the answer simply by doing a sum,
                        # but it also means we have no way to visualize this.
                        self.contents[coord[1] * self.width + coord[0]] = 0

        return changed

    def search_for_sea_monsters(self):
        skip = False
        for i in range(4):
            if self._search_for_sea_monsters_subroutine():
                skip = True
                break
            self.rotation = Direction.EAST
            self.perma_rotate()
        self.flipped = True
        self.perma_rotate()
        for i in range(4):
            if skip or self._search_for_sea_monsters_subroutine():
                break
            self.rotation = Direction.EAST
            self.perma_rotate()

        print("Part 2: Water roughness", sum(self.contents))

# -- END TILES SUBSECTION -- #


class Image:
    def __init__(self, tilepool: list[Tile]):
        self.tilepool = tilepool
        tilepool[0].location = (0, 0)
        self.layout = {(0, 0): tilepool[0]}
        self.tile_size = self.tilepool[0].width
        self.full_layout = ""
        self.part_1_answer = 0
        queue = q.SimpleQueue()
        queue.put(tilepool[0])

        while not queue.empty():
            tile: Tile = queue.get()
            for other_tile in tilepool:
                if other_tile.location is None and tile.place_if_border_matches(other_tile):
                    self.layout[other_tile.location] = other_tile  # it won't be None anymore here
                    queue.put(other_tile)

        self.finalize()
        self.full_layout = Tile("Tile 0000:\n" + self.full_layout.strip())

    def __str__(self):
        # for key in sorted(self.layout.keys(), key=self._tile_location_compare):
        return self.layout.__str__()

    def finalize(self):
        coords = {}
        x_set = set()
        for key in self.layout.keys():
            x_set.add(key[0])
            if key[1] in coords:
                coords[key[1]].append(key)
            else:
                coords[key[1]] = [key]

        for y in sorted(coords.keys()):
            coords[y].sort()
            for j in range(1, self.tile_size - 1):
                for coord in coords[y]:
                    for i in range(1, self.tile_size - 1):
                        self.full_layout += "#" if self.layout[coord][i, j] == 1 else "."
                self.full_layout += "\n"

        # print(self.full_layout)

        x_min = min(x_set)
        x_max = max(x_set)
        y_min = min(coords.keys())
        y_max = max(coords.keys())
        self.part_1_answer = int(self.layout[x_min, y_min].tile_id) * int(self.layout[x_max, y_min].tile_id) \
            * int(self.layout[x_min, y_max].tile_id) * int(self.layout[x_max, y_max].tile_id)

        print("Part 1: Product of corners: ", self.part_1_answer)


def parse_input(filename: str):
    with open(filename, "r") as file:
        tile_strings = file.read().strip().split("\n\n")
        tiles = []
        for tile_string in tile_strings:
            tiles.append(Tile(tile_string))

    return tiles


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    start_time = time.time()
    tiles = parse_input(input_filename)
    part1_start = time.time()
    image = Image(tiles)
    part2_start = time.time()
    image.full_layout.search_for_sea_monsters()
    end_time = time.time()
    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2020/day20.txt"
        main(filename)

    run_main()
