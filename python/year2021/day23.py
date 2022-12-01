import time
import os
import collections
import re
import enum
import copy


class Tile(enum.Enum):
    WALL = -1
    EMPTY = 0
    A = 1
    B = 10
    C = 100
    D = 1000


TILE_STRINGS = {"A": Tile.A, "B": Tile.B, "C": Tile.C, "D": Tile.D,
                Tile.A: "A", Tile.B: "B", Tile.C: "C", Tile.D: "D", Tile.WALL: "#", Tile.EMPTY: " "}
Point = collections.namedtuple("Point", ["x", "y"])
Amphipod = collections.namedtuple("Amphipod", ["pos", "type", "locked"])
Move = collections.namedtuple("Move", ["amphipod", "end_pos", "cost"])
ROOMS_X = [3, 5, 7, 9]
ROOMS_Y = [2, 3, 4, 5]
ROOMS_ID = {3: Tile.A, 5: Tile.B, 7: Tile.C, 9: Tile.D}
ROOMS_X_FROM_TYPE = {Tile.A: 3, Tile.B: 5, Tile.C: 7, Tile.D: 9}
TYPES = [Tile.A, Tile.B, Tile.C, Tile.D]


class Layout:
    # Parts for assembling the layout
    LOWER_RM = [Tile.EMPTY, Tile.EMPTY, Tile.WALL, Tile.A, Tile.WALL, Tile.B, Tile.WALL, Tile.C, Tile.WALL, Tile.D,
                Tile.WALL, Tile.EMPTY, Tile.EMPTY]
    UPPER_RM = [Tile.WALL, Tile.WALL, Tile.WALL, Tile.A, Tile.WALL, Tile.B, Tile.WALL, Tile.C, Tile.WALL, Tile.D,
                Tile.WALL, Tile.WALL, Tile.WALL]
    WALL = [Tile.WALL] * 13
    HALL = [Tile.WALL, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY,
            Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.WALL]
    LOWER_WALL = [Tile.EMPTY, Tile.EMPTY, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL,
                  Tile.WALL, Tile.WALL, Tile.EMPTY, Tile.EMPTY]
    ADJACENT = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]

    assert len(LOWER_RM) == 13
    assert len(UPPER_RM) == 13
    assert len(WALL) == 13
    assert len(HALL) == 13
    assert len(LOWER_WALL) == 13

    def __init__(self, sequence: list[Tile], part: int):
        self.size_x = 13
        self.size_y = 5 if part == 1 else 7
        self.room_size = 2 if part == 1 else 4
        self.walls = []
        self.objects = [Tile.EMPTY for _ in range(self.size_x * self.size_y)]
        for i in Layout.WALL:
            self.walls.append(i)
        for i in Layout.HALL:
            self.walls.append(i)
        for i in Layout.UPPER_RM:
            self.walls.append(i)
        for n in range(self.room_size - 1):
            for i in Layout.LOWER_RM:
                self.walls.append(i)
        for i in Layout.LOWER_WALL:
            self.walls.append(i)
        self.amphipods = set()  # Note that this is some data redundancy, so we can easily look up an Amphipod's pos

        def init_objects():  # so this literally just exists so we can break out of the nesting with return.
            j = 0
            lim = len(sequence)
            for y in ROOMS_Y:
                for x in ROOMS_X:
                    self.objects[self.get_index(x, y)] = sequence[j]
                    self.amphipods.add(Amphipod(Point(x, y), sequence[j], False))
                    j += 1
                    if j == lim:
                        return

        init_objects()
        self.get_locked_amphipods()
        self.min_costs = dict()
        self.fill_minimum_costs_dict()

    def __repr__(self):
        x = 0
        output = ""
        for i, tile in enumerate(self.walls):
            if tile == Tile.WALL:
                output += "#"
            else:
                try:
                    output += TILE_STRINGS[self.objects[i]]
                except IndexError:
                    print(f"Complaining about {i} -- max is {len(self.objects) - 1}")
            x += 1
            if x == self.size_x:
                x = 0
                output += "\n"
        output += "\n"
        return output

    def get_point(self, index: int):
        x = index % self.size_x
        y = index // self.size_x
        return Point(x, y)

    def get_index(self, x: int, y: int) -> int:
        return x + (y * self.size_x)

    def pt_index(self, pt: Point):  # unfortunately no function overloading in Python
        return self.get_index(pt.x, pt.y)

    def get_locked_amphipods(self):
        for amphipod in self.amphipods:
            if amphipod.locked:
                continue
            self.update_amphipod_locked(amphipod)

    def update_amphipod_locked(self, amphipod):
        if (amphipod.pos.x in ROOMS_X) and (amphipod.pos.y in ROOMS_Y) and (ROOMS_ID[amphipod.pos.x] == amphipod.type):
            index_below = self.get_index(amphipod.pos.x, amphipod.pos.y + 1)
            # debug_info = [amphipod.pos.y + 1]
            # try:
            while True:
                if self.walls[index_below] == Tile.WALL:
                    # print("It has to be this line.")
                    self.amphipods.remove(amphipod)
                    self.amphipods.add(Amphipod(amphipod.pos, amphipod.type, True))
                    # print("IT'S FUCKING LOCKED")
                    return
                if self.objects[index_below] != amphipod.type:
                    return
                index_below = self.get_point(index_below)
                # debug_info.append(index_below.y + 1)
                index_below = self.get_index(index_below.x, index_below.y + 1)
            # except IndexError as e:
            #     print("Bad things happened!")
            #     print(f"Amphipod: {amphipod}, checking tile {self.get_point(index_below)}")
            #     print(f"which is at index {index_below}, and the maximum index was {len(self.walls)}")
            #     print(f"The maximum y is {self.size_y}; tried y = {debug_info}")
            #     raise e
            # except KeyError as e:
            #     print("Bad things happened!")
            #     print(f"Amphipod: {amphipod}, checking tile {self.get_point(index_below)}")
            #     print(f"Because this is FUCKING CURSED the wall status of this tile is {self.walls[index_below]}")
            #     print(self)
            #     print(self.amphipods)
            #     raise e

    @property
    def win(self):
        for amphipod in self.amphipods:
            if not amphipod.locked:
                return False
        return True

    # Generates the possible moves a given amphipod can make. Returns the set of moves, and a boolean that shows if
    # the move would place an amphipod in its correct position (only 1 move can be in the set if this boolean is True)
    def generate_moves(self, amphipod: Amphipod) -> (set[Move], bool):
        costs = [0] * len(self.objects)
        if amphipod.locked:
            return set(), False
        moves = set()
        st_index = self.pt_index(amphipod.pos)
        atype = self.objects[st_index]
        cost = atype.value
        if atype == Tile.EMPTY:
            raise RuntimeError(f"Layout.generate_moves: No object at ({amphipod.pos.x}, {amphipod.pos.y})")
        elif atype == Tile.WALL:
            raise RuntimeError(f"Layout.generate_moves: Invalid object type at ({amphipod.pos.x}, {amphipod.pos.y})")
        pt_queue = [amphipod.pos]
        while len(pt_queue) > 0:
            ref_pt = pt_queue.pop(0)
            current_cost = costs[self.pt_index(ref_pt)] + cost
            for neighbor in Layout.ADJACENT:
                pt = Point(neighbor.x + ref_pt.x, neighbor.y + ref_pt.y)
                pt_index = self.pt_index(pt)
                # The original has a check for being in bounds, but it seems safe to assume that it's redundant.
                # It will need to be included in this if statement if it turns out not to be redundant, though.
                if self.walls[pt_index] != Tile.WALL \
                        and self.objects[pt_index] == Tile.EMPTY \
                        and (costs[pt_index] > current_cost or costs[pt_index] == 0):
                    # There's another condition going on something about hallways, but I think it doesn't actually
                    # do anything...
                    pt_queue.append(pt)
                    costs[pt_index] = current_cost
                    # moves.add(Move(amphipod, pt, current_cost))

        # print(f"Moves before purging: {len(moves)}: {moves}")

        # Remove bad moves
        def no_entry_room(room_x: int):
            for _y in ROOMS_Y[:self.room_size]:
                # moves.discard(Move(amphipod, Point(room_x, _y), costs[self.get_index(room_x, _y)]))
                costs[self.get_index(room_x, _y)] = 0

        for x in ROOMS_X:
            costs[self.get_index(x, 1)] = 0
            moves.discard(Move(amphipod, Point(x, 1), costs[self.get_index(x, 1)]))
            if ROOMS_ID[x] != atype:
                no_entry_room(x)
            else:  # You can only enter the back of the room
                # debug = []
                for y in reversed(ROOMS_Y[:self.room_size]):
                    # debug.append(y)
                    i = self.get_index(x, y)
                    if self.objects[i] == Tile.EMPTY and costs[i] != 0:
                        # There's never a reason not to go into position if we're allowed to,
                        # so if this move is available, then we just return this move
                        cost = costs[i]
                        '''print(debug)
                        if len(debug) == 2:
                            print(self.objects)
                            bad_point = Point(x, y + 1)
                            bad_index = self.pt_index(bad_point)
                            assert self.objects[bad_index] != Tile.EMPTY
                            print(f"So we're trying to figure out wtf is going on with {Point(x, y)}")
                            print(f"which is currently {self.objects[i]}")
                            print(f"and below it is {bad_point}, which is currently {self.objects[bad_index]}")
                            print(self)'''
                        return {Move(amphipod, Point(x, y), cost)}, True
                    elif self.objects[i] != atype:
                        no_entry_room(x)
                        break
        # No hallways if you're already in the hallway.
        if amphipod.pos.y == 1:
            for x in range(1, self.size_x - 1):
                # moves.discard(Move(amphipod, Point(x, 1), costs[self.get_index(x, 1)]))
                costs[self.get_index(x, 1)] = 0
        # print(f"Moves after purging: {len(moves)}: {moves}\n")
        for i, cost in enumerate(costs):
            if costs[i] != 0:
                moves.add(Move(amphipod, self.get_point(i), costs[i]))
        return moves, False

    def get_minimum_fuel_requirements(self):
        total = 0
        locked = collections.Counter()
        for amphipod in self.amphipods:
            if not amphipod.locked:
                total += self.min_costs[amphipod.type][self.pt_index(amphipod.pos)]
            else:
                locked[amphipod.type] += 1
        #   i cannot think right now so this isn't finished
        # how the fuck do I account for diff destinations and shit

    def fill_minimum_costs_dict(self):
        def get_costs(destination: Point, cost: int):
            costs = []
            pt_queue = [destination]
            while len(pt_queue) > 0:
                ref_pt = pt_queue.pop(0)
                current_cost = costs[self.pt_index(ref_pt)] + cost
                for neighbor in Layout.ADJACENT:
                    pt = Point(neighbor.x + ref_pt.x, neighbor.y + ref_pt.y)
                    pt_index = self.pt_index(pt)
                    if self.walls[pt_index] != Tile.WALL \
                            and (costs[pt_index] > current_cost or costs[pt_index] == 0):
                        pt_queue.append(pt)
                        costs[pt_index] = current_cost
            return costs
        dest_y = 3 if self.size_y == 5 else 5
        for atype in TYPES:
            self.min_costs[atype] = get_costs(Point(ROOMS_X_FROM_TYPE[atype], dest_y), atype.value)

    def move(self, move: Move):
        # Note that this does not *validate* the move, at least not much
        assert not move.amphipod.locked
        start_index = self.pt_index(move.amphipod.pos)
        self.objects[self.pt_index(move.end_pos)] = self.objects[start_index]
        self.objects[start_index] = Tile.EMPTY
        new_amphipod = Amphipod(move.end_pos, move.amphipod.type, False)
        self.amphipods.remove(move.amphipod)
        self.amphipods.add(new_amphipod)
        self.update_amphipod_locked(new_amphipod)
        assert self.objects[self.pt_index(new_amphipod.pos)] == new_amphipod.type


class BFS:
    score = None  # ugly hack put in later

    def __init__(self, layout: Layout, usage: int = 0, parent=None, d=1):
        self.dead_end = False
        self.usage = usage
        self.score = None
        self.layout: Layout = layout
        self.children = None
        self.parent = parent
        self.d = d

    def get_all_moves(self, depth):
        moves = set()
        for amphipod in self.layout.amphipods:
            amph_moves, go_to_room = self.layout.generate_moves(amphipod)
            # If an amphipod is able to go to its proper room, there is no reason not to just go ahead and do it.
            if go_to_room:
                return amph_moves
            moves = moves.union(amph_moves)
        # print(f"get_all_moves: {len(moves)}: {moves}")
        if len(moves) == 0:
            print("ASDFASDFGLKASJHDFGHLKSDFJHGSDFGH depth =", depth)
        return moves

    def search(self, max_depth=-1):
        depth = 0
        while not self.dead_end and max_depth != 0:
            depth += 1
            print("---------------------------------------")
            print("Searching at depth", depth)
            self.search_next_level(depth)
            max_depth -= 1
        return self.score

    def search_next_level(self, depth):
        if self.dead_end:
            print("dead end")
            return None
        if self.children is None:
            # print("Branch 1")
            self.children = []
            moves = self.get_all_moves(depth)
            # print("Moves:", moves)
            if len(moves) == 0:
                self.dead_end = True
                return None
            for move in moves:
                new_layout = copy.deepcopy(self.layout)
                new_layout.move(move)
                new_usage = self.usage + move.cost
                if new_layout.win:
                    print(f"Found winning configuration with usage: {new_usage}")
                    self.score = min(self.score, new_usage) if self.score is not None else new_usage
                    BFS.score = min(BFS.score, new_usage) if BFS.score is not None else new_usage
                else:
                    # print(new_layout)
                    self.children.append(BFS(new_layout, new_usage, self, self.d + 1))
            return self.score
        # enumerate won't work here because we need the actual index, but also while going in reverse...
        live_child_branch = False
        for i in range(len(self.children) - 1, -1, -1):
            child = self.children[i]
            if child.dead_end:
                print(f"child dead end - used {child.usage}, d={child.d}")
                if child.usage == 30:
                    child.report_chain()
                del self.children[i]  # ...because we want to delete stuff while we're iterating
                continue
            if BFS.score is not None and child.usage > BFS.score:
                print(f"branch culled due to excessive ({child.usage}) fuel usage")
                del self.children[i]
                continue
            live_child_branch = True
            try:
                result = child.search_next_level(depth)
            except KeyError:
                print(self.layout)
                raise KeyError
            if result is not None:
                self.score = min(self.score, result) if self.score is not None else result
                BFS.score = min(BFS.score, result) if BFS.score is not None else result
        if not live_child_branch:
            self.dead_end = True
        return self.score

    def report_chain(self):
        print(self.layout)
        if self.parent is not None:
            self.parent.report_chain()


class DFS:
    score = None

    def __init__(self, layout: Layout, usage = 0):
        self.layout = layout
        self.usage = usage

    def search(self, depth=0):
        if self.layout.win:
            print(f"Found winning configuration with usage: {self.usage} in {depth} moves")
            DFS.score = min(self.usage, DFS.score) if DFS.score is not None else self.usage
        moves = self.get_all_moves()
        if len(moves) > 0:
            for move in sorted(moves, key=lambda x: x.cost):
                # if DFS.score is None or DFS.score > self.usage + move.cost:
                if DFS.score is not None and DFS.score < self.usage + move.cost:
                    print(f"Tossed at {self.usage + move.cost} due to excessive fuel usage.")
                    break
                new_layout = copy.deepcopy(self.layout)
                new_layout.move(move)
                DFS(new_layout, self.usage + move.cost).search(depth + 1)
        # else:
            # print(f"Dead end hit at usage: {self.usage}, depth {depth}")
        return DFS.score

    def get_all_moves(self):
        moves = set()
        for amphipod in self.layout.amphipods:
            amph_moves, go_to_room = self.layout.generate_moves(amphipod)
            # If an amphipod is able to go to its proper room, there is no reason not to just go ahead and do it.
            if go_to_room:
                return amph_moves
            moves = moves.union(amph_moves)
        # print(f"get_all_moves: {len(moves)}: {moves}")
        return moves


def input_to_string(filename: str):
    with open(filename, "r") as file:
        return file.read()


def construct_part_2_input(string: str):
    output = ""
    for i, line in enumerate(string.strip().split("\n")):
        if i == 3:
            output += "  #D#C#B#A#\n  #D#B#A#C#\n"
        output += f"{line}\n"
    return output


def parse_input(string: str, part: int):
    regex = re.compile(r"[ABCD]")
    sequence = []
    for match in regex.findall(string):
        print(f"{match}, {TILE_STRINGS[match]} = {TILE_STRINGS[match].value}")
        sequence.append(TILE_STRINGS[match])
    return Layout(sequence, part)


def test():
    print("TEST FOR STUFF!")
    layout = parse_input("DABABCDC", 1)
    layout.amphipods = \
        {
            Amphipod(Point(3, 3), Tile.C, False),
            Amphipod(Point(4, 1), Tile.D, False),
            Amphipod(Point(6, 1), Tile.C, False),
            Amphipod(Point(8, 1), Tile.D, False),
            Amphipod(Point(9, 2), Tile.B, False),
            Amphipod(Point(5, 3), Tile.A, False),
            Amphipod(Point(7, 3), Tile.A, False),
            Amphipod(Point(9, 3), Tile.B, False),
        }
    layout.objects = [Tile.EMPTY] * len(layout.objects)
    for amphipod in layout.amphipods:
        layout.objects[layout.pt_index(amphipod.pos)] = amphipod.type
    bfs = BFS(layout, usage=4520)
    moves = bfs.get_all_moves(0)
    print(moves)
    print(layout)
    assert len(moves) == 4


def main(input_filename: str):
    # Dummy out this very slow day.
    return -1
    input_string = input_to_string(input_filename)
    print(input_string)
    layout = parse_input(input_string, 1)
    print(layout)
    print("-------------------------")
    test()
    '''input_string_2 = construct_part_2_input(input_string)
    print(input_string_2)
    print(parse_input(input_string_2, 2))
    print("-------------------------")'''
    score = DFS(layout).search()
    print(f"Score: {score}")
    return -1


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day23.txt")
