module year2023.day14;

import std.conv;
import std.regex;
import std.string;
import std.stdio;
import std.exception;
import std.algorithm;
import std.array;
import core.time;

import utility;
import input;

alias Grid = Grid2D!Tile;
alias Pt = Point!int;

enum Tile: char
{
    Round = 'O',
    Cube = '#',
    Empty = '.'
}

Grid parse_input()
{ 
    Pt size;
    Tile[] layout;
    // Probably would have been better to iterate through the lines but doing like this
    // allowed just copy/pasting from Day 13 and tweaking a full things. Another case
    // where there's a common pattern with *just enough* variance to make it hard to DRY.
    auto pattern = get_input(2023, 14);
    auto lines = pattern.strip.split(regex("\r?\n"));
    size.y = lines.length.to!int;
    foreach(line; lines) {
        if (size.x == 0) size.x = line.length.to!int;
        enforce(size.x == line.length.to!int, "Bad input.");
        foreach(c; line) {
            layout ~= c.to!Tile;
        }
    }
    return new Grid(size, layout);
}

enum Direction { North, South, East, West }
void simulate_rocks(Direction d)(ref Grid grid)
{
    // This looks a bit nasty, but the alternatives were:
    //    -- subfunction with super convoluted arguments that would be difficult to reason about,
    //       especially if it doesn't work on the first try.
    //    -- manually copy/pasting the function 4 times and changing these 3 lines in each one.
    static if (d == Direction.North) {
        enum outer_loop = "foreach(y; 1..grid.size.y)";
        enum inner_loop = "foreach(x; 0..grid.size.x)";
        enum call_move_rock = "move_rock!(-1)(source, 0, -grid.size.x);";
    }
    else static if (d == Direction.West) {
        enum outer_loop = "foreach(x; 1..grid.size.x)";
        enum inner_loop = "foreach(y; 0..grid.size.y)";
        enum call_move_rock = "move_rock!(-1)(source, y * grid.size.x, -1);";
    }
    else static if (d == Direction.South) {
        enum outer_loop = "for(int y = grid.size.y - 2; y >= 0; --y)";
        enum inner_loop = "foreach(x; 0..grid.size.x)";
        enum call_move_rock = "move_rock!(1)(source, grid.layout.length, grid.size.x);";
    }
    else static if (d == Direction.East) {
        enum outer_loop = "for(int x = grid.size.x - 2; x >= 0; --x)";
        enum inner_loop = "foreach(y; 0..grid.size.y)";
        enum call_move_rock = "move_rock!(1)(source, (y + 1) * grid.size.x, 1);";
    }
    else static assert (0);

    void move_rock(int sign)(size_t start, size_t stop, int step) 
    {
        static if (sign > 0) enum loop = "for(size_t i = start; i < stop; i += step)";
        else static if (sign < 0) enum loop = "for(int i = start.to!int; i >= stop.to!int; i += step)";
        else static assert(0);
        size_t last = start;
        grid.layout[start] = Tile.Empty;
        mixin(
        loop ~ " {
            if (grid.layout[i] != Tile.Empty) {
                grid.layout[last] = Tile.Round;
                return;
            }
            last = i;
        }
        ");
        grid.layout[last] = Tile.Round;
        return;
    }

    mixin(
    outer_loop ~ " {
        " ~ inner_loop ~ " {
            size_t source = grid.index_at_pt(Pt(x, y));
            if (grid.layout[source] == Tile.Round) " ~ call_move_rock ~ "
        }
    }");
    return;
}

void run_simulation(ref Grid grid)
{
    grid.simulate_rocks!(Direction.North);
    return;
}

// Each run does one cycle.
void run_simulation_pt2(ref Grid grid)
{
    grid.simulate_rocks!(Direction.North);
    grid.simulate_rocks!(Direction.West);
    grid.simulate_rocks!(Direction.South);
    grid.simulate_rocks!(Direction.East);
    return;
}

int calculate_load(const ref Grid grid)
{
    int total = 0;
    foreach(i, tile; grid.layout) {
        if (tile == Tile.Round) {
            int y = i.to!int / grid.size.x;
            total += grid.size.y - y;
        }
    }
    return total;
}

int part_1(Grid grid) 
{
    grid.run_simulation;
    return grid.calculate_load;
}

int part_2(Grid grid)
{
    size_t[string] cache;
    // string[size_t] grid_cache;  // probably not the most RAM friendly thing in the world, but it's cheap
    string[] grid_cache;
    // If we wanted to be a bit more stringent with RAM we could just calculate the loads each iteration
    // and then only take the one we need.
    auto runs = 1_000_000_000;
    foreach(i; 0..runs) {
        grid.run_simulation_pt2;
        auto str = grid.stringify;
        size_t* ptr = str in cache;
        if (ptr is null) {
            cache[str] = i;
            grid_cache ~= str;
        }
        else {
            writefln("We've visited here before: Cycle %s (it is now Cycle %s)", *ptr, i);
            size_t last_index = (runs - 1 - *ptr) % (i - *ptr) + *ptr;
            grid = grid_cache[last_index].unstringify(grid.size);
            return grid.calculate_load;
        }
    }
    return grid.calculate_load;
}

string stringify(const ref Grid grid)
{
    return grid.layout.map!(a=>a.to!char).to!string;
}

Grid unstringify(string str, Pt size)
{
    return new Grid(size, str.map!(c=>c.to!Tile).array);
}

bool run_2023_day14()
{
    auto start_time = MonoTime.currTime;
    auto grid = parse_input;
    auto gridpt2 = new Grid(grid.size, grid.layout.dup);
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(grid);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(gridpt2);
    auto end_time = MonoTime.currTime;

    writefln("Total load (part 1): %s", pt1_solution);
    writefln("Total load (part 2): %s", pt2_solution);

    writeln("Elapsed Time:");
    writefln("    Parsing: %s ms", float((pt1_start - start_time).total!"usecs") / 1000);
    writefln("    Part 1: %s ms", float((pt2_start - pt1_start).total!"usecs") / 1000);
    writefln("    Part 2: %s ms", float((end_time - pt2_start).total!"usecs") / 1000);
    writefln("    Total: %s ms", float((end_time - start_time).total!"usecs") / 1000);

    return true;
}

void pretty_print(Grid grid)
{
    writefln("Grid2D: %s by %s", grid.size.x, grid.size.y);
    foreach (y; 0..grid.size.y) {
        foreach(x; 0..grid.size.x) {
            write(grid[x, y].to!char);
        }
        writeln;
    }
    return;
}