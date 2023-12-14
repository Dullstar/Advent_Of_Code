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
int simulate_rocks(Direction d)(ref Grid grid)
{
    // This looks a bit nasty, but the alternatives were:
    //    -- subfunction with super convoluted arguments that would be difficult to reason about,
    //       especially if it doesn't work on the first try.
    //    -- manually copy/pasting the function 4 times and changing these 3 lines in each one.
    int total = 0;
    static if (d == Direction.North) {
        enum outer_loop = "foreach(y; 1..grid.size.y)";
        enum inner_loop = "foreach(x; 0..grid.size.x)";
        enum dest_pt = "x, y - 1";
    }
    else static if (d == Direction.West) {
        enum outer_loop = "foreach(x; 1..grid.size.x)";
        enum inner_loop = "foreach(y; 0..grid.size.y)";
        enum dest_pt = "x - 1, y";
    }
    else static if (d == Direction.South) {
        enum outer_loop = "foreach(y; 0..grid.size.y - 1)";
        enum inner_loop = "foreach(x; 0..grid.size.x)";
        enum dest_pt = "x, y + 1";
    }
    else static if (d == Direction.East) {
        enum outer_loop = "foreach(x; 0..grid.size.x - 1)";
        enum inner_loop = "foreach(y; 0..grid.size.y)";
        enum dest_pt = "x + 1, y";
    }
    else static assert (0);

    mixin(
    outer_loop ~ " {
        " ~ inner_loop ~ " {
            size_t source = grid.index_at_pt(Pt(x, y));
            if (grid.layout[source] == Tile.Round) {
                size_t dest = grid.index_at_pt(Pt(" ~ dest_pt ~ "));
                if (grid.layout[dest] == Tile.Empty) {
                    grid.layout[source] = Tile.Empty;
                    grid.layout[dest] = Tile.Round;
                    total += 1;
                }
            }
        }
    }");
    return total;
}

void run_simulation(ref Grid grid)
{
    while (simulate_rocks!(Direction.North)(grid)) {}
    return;
}

// Each run does one cycle.
void run_simulation_pt2(ref Grid grid)
{
    while (grid.simulate_rocks!(Direction.North)) {}
    while (grid.simulate_rocks!(Direction.West)) {}
    while (grid.simulate_rocks!(Direction.South)) {}
    while (grid.simulate_rocks!(Direction.East)) {}
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
    string[size_t] grid_cache;  // probably not the most RAM friendly thing in the world, but it's cheap
    // If we wanted to be a bit more stringent with RAM we could just calculate the loads each iteration
    // and then only take the one we need.
    // int[] sizes;
    // okay, like no chance this works but let's see how bad we're talking.
    auto runs = 1_000_000_000;
    foreach(i; 0..runs) {
        grid.run_simulation_pt2;
        auto str = grid.stringify;
        size_t* ptr = str in cache;
        if (ptr is null) {
            cache[str] = i;
            grid_cache[i] = str;
            // sizes ~= grid.calculate_load;
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
    auto gridpt2 = parse_input;  // awful hack to clone this easily
    auto pt1_start = MonoTime.currTime;
    auto pt1_solution = part_1(grid);
    auto pt2_start = MonoTime.currTime;
    auto pt2_solution = part_2(gridpt2);
    auto end_time = MonoTime.currTime;

    writefln("Result of reflections (part 1): %s", pt1_solution);
    writefln("Result of flawed reflections (part 2): %s", pt2_solution);

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